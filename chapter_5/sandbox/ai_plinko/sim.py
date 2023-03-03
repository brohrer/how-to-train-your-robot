import json
import time
from numba import njit
import numpy as np
import logging_setup
from pacemaker import Pacemaker
import config
from damper import Damper


def run(q):
    logger = logging_setup.get_logger("sim", config.LOGGING_LEVEL_SIM)
    sim = Simulation()
    pacemaker = Pacemaker(config.CLOCK_FREQ_SIM)

    # Updating the q can slow down the simulation.
    # Converting the terrain array to JSON is a slow process.
    # Only update it approximately twice per frame.
    # Once per frame might lead to lost-frame glitches, which could
    # be noticeable.
    steps_per_q_update = int(
        config.CLOCK_FREQ_SIM / (2 * config.CLOCK_FREQ_VIZ)
    )
    steps_since_q_update = 0

    i_over = 0.0
    i_total = 0.0
    while True:
        overtime = pacemaker.beat()

        i_total += 1
        if overtime > config.CLOCK_PERIOD_SIM * 0.5:
            i_over += 1
            print(
                f"over {overtime / config.CLOCK_PERIOD_SIM}     {i_over / i_total}"
            )

        if overtime > config.CLOCK_PERIOD_SIM:
            logger.error(json.dumps({"ts": time.time(), "overtime": overtime}))

        state = sim.step()
        ts = time.time()

        steps_since_q_update += 1
        if steps_since_q_update >= steps_per_q_update:
            logger.debug(json.dumps({"ts": ts, "state": state}))
            q.put((ts, state))
            steps_since_q_update = 0


class Simulation:
    def __init__(self):
        # Initialize all the discs
        self.x = []
        self.y = []
        self.vx = []
        self.vy = []
        self.r = []
        self.k = []
        self.m = []
        self.n_discs = 0

        self.x_wall = []
        self.y_wall = []
        self.x_n = []
        self.y_n = []
        self.n_walls = 0

        self.i_puck = self.add_disc(
            k=config.PUCK_STIFFNESS,
            m=config.PUCK_MASS,
            r=config.PUCK_RADIUS,
            x=config.PUCK_X,
            y=config.PUCK_Y,
        )

        # Create the array of pegs
        i_pegs = []
        self.peg_state = {}
        for i_row in range(config.N_PEG_ROWS):
            peg_y = (
                config.PEG_BOTTOM_SPACING
                + (2 * i_row + 1) * config.PEG_RADIUS
                + i_row * config.PEG_ROW_SPACING
            )
            # Half-column shift every other row
            shift = (
                (i_row % 2)
                * (config.PEG_COL_SPACING + 2 * config.PEG_RADIUS)
                / 2
            )
            for i_col in range(config.N_PEG_COLS):
                peg_x = (
                    shift
                    + config.PEG_EDGE_SPACING
                    + (2 * i_col + 1) * config.PEG_RADIUS
                    + i_col * config.PEG_COL_SPACING
                )
                i_peg = self.add_disc(
                    k=config.PEG_STIFFNESS,
                    r=config.PEG_RADIUS,
                    x=peg_x,
                    y=peg_y,
                )
                i_pegs.append(i_peg)
                self.peg_state[i_peg] = {"x": peg_x, "y": peg_y}

        self.add_wall(
            x_left=0.0,
            y_left=0.0,
            x_right=0.0,
            y_right=1.0,
        )
        self.add_wall(
            x_left=config.FIG_WIDTH,
            y_left=1.0,
            x_right=config.FIG_WIDTH,
            y_right=0.0,
        )
        self.damper = Damper(
            x=config.PUCK_X,
            y=config.PUCK_Y,
            damping=config.DAMPING,
        )

        self.x = np.array(self.x)
        self.y = np.array(self.y)
        self.x_n = np.array(self.x_n)[:, np.newaxis]
        self.y_n = np.array(self.y_n)[:, np.newaxis]
        self.x_wall = np.array(self.x_wall)
        self.y_wall = np.array(self.y_wall)
        self.vx = np.array(self.vx)
        self.vy = np.array(self.vy)
        self.r = np.array(self.r)
        self.k = np.array(self.k)
        self.m = np.array(self.m)
        self.fx_disc = np.zeros(self.n_discs)
        self.fy_disc = np.zeros(self.n_discs)
        self.fx_disc_disc = np.zeros((self.n_discs, self.n_discs))
        self.fy_disc_disc = np.zeros((self.n_discs, self.n_discs))
        self.fx_wall_disc = np.zeros((self.n_walls, self.n_discs))
        self.fy_wall_disc = np.zeros((self.n_walls, self.n_discs))

        self.r_disc_disc = np.tile(
            self.r[:, np.newaxis], (1, self.n_discs)
        ) + np.tile(self.r[np.newaxis, :], (self.n_discs, 1))
        self.k_disc_disc = 1 / (
            (1 / np.tile(self.k[:, np.newaxis], (1, self.n_discs)))
            + (1 / np.tile(self.k[np.newaxis, :], (self.n_discs, 1)))
        )
        # Set the diagonal to zeros so that no disc tries
        # to interact with itself.
        self.k_disc_disc[
            np.arange(self.n_discs), np.arange(self.n_discs)
        ] = 0.0
        self.row_tile = np.ones((self.n_discs, 1))
        self.col_tile = np.ones((1, self.n_discs))

    def add_disc(self, m=1.0, r=1.0, k=1.0, x=0.0, y=0.0, vx=0.0, vy=0.0):
        self.m.append(m)
        self.r.append(r)
        self.k.append(k)
        self.x.append(x)
        self.y.append(y)
        self.vx.append(vx)
        self.vy.append(vy)
        self.n_discs += 1
        return int(self.n_discs - 1)

    def add_wall(self, x_left, y_left, x_right, y_right):
        """
        Initialize with two points on the line.
        Imagine you are looking at the wall.
        One point will be on the left (x_left, y_left)
        and the other will be on the right (x_right, y_right).
        """
        # A unit vector normal to the surface of the wall
        # pointing away from the wall.
        x_normal, y_normal = self.calculate_wall_normal(
            x_left, y_left, x_right, y_right
        )
        # An arbitrary point on the line
        self.x_wall.append(x_left)
        self.y_wall.append(y_left)
        self.x_n.append(x_normal)
        self.y_n.append(y_normal)
        self.n_walls += 1
        return int(self.n_walls)

    def calculate_wall_normal(self, x_left, y_left, x_right, y_right):
        dist_lr = ((x_left - x_right) ** 2 + (y_left - y_right) ** 2) ** 0.5
        epsilon = 1e-12
        if dist_lr < epsilon:
            raise ValueError("Left and right points need to be further apart")

        x_normal = (y_right - y_left) / dist_lr
        y_normal = (x_left - x_right) / dist_lr
        return (x_normal, y_normal)

    def step(self):
        self.calculate_forces()

        # Set the forces on all the pins to 0 so they will stay put.
        self.fx_disc[self.i_puck + 1 :] = 0.0
        self.fy_disc[self.i_puck + 1 :] = 0.0

        self.update_positions()
        state = self.get_state()
        return state

    def get_state(self):
        return {
            "puck": self.get_puck_state(),
            "pegs": self.peg_state,
            "damper": self.damper.get_state(),
        }

    def get_puck_state(self):
        return {
            "x": self.x[self.i_puck],
            "y": self.y[self.i_puck],
            "vx": self.vx[self.i_puck],
            "vy": self.vy[self.i_puck],
        }

    def disc_disc_interactions(self):
        disc_disc_interaction_numba(
            self.col_tile,
            self.row_tile,
            self.fx_disc_disc,
            self.fy_disc_disc,
            self.k_disc_disc,
            self.r_disc_disc,
            self.x[:, np.newaxis],
            self.x[np.newaxis, :],
            self.y[:, np.newaxis],
            self.y[np.newaxis, :],
        )

    def disc_wall_interactions(self):
        """
        Taken from
        https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
        and modfied to the form
        d = (x - x1) * x_normal + (y - y1) * y_normal
        where (x1, y1) is any point on the line.

        This is a signed distance.
        A positive value indicates distance away from the wall.
        A negative value indicates distance *into* the wall.
        """
        dx = np.tile(self.x[np.newaxis, :], (self.n_walls, 1)) - np.tile(
            self.x_wall[:, np.newaxis], (1, self.n_discs)
        )
        dy = np.tile(self.y[np.newaxis, :], (self.n_walls, 1)) - np.tile(
            self.y_wall[:, np.newaxis], (1, self.n_discs)
        )
        dx_n = dx * self.x_n
        dy_n = dy * self.y_n
        distance = np.abs(dx_n) + np.abs(dy_n)
        compression = self.r - distance
        compression = np.maximum(compression, 0)

        f_mag = self.k[np.newaxis, :] * compression
        f_norm = f_mag / distance
        self.fx_wall_disc += f_norm * self.x_n
        self.fy_wall_disc += f_norm * self.y_n

    def calculate_forces(self):
        self.fx_disc = 0.0
        self.fy_disc = 0.0
        self.fx_disc_disc = np.zeros((self.n_discs, self.n_discs))
        self.fy_disc_disc = np.zeros((self.n_discs, self.n_discs))
        self.fx_wall_disc = 0.0
        self.fy_wall_disc = 0.0

        self.disc_disc_interactions()
        self.disc_wall_interactions()

        self.fx_disc += np.sum(self.fx_disc_disc, axis=0)
        self.fy_disc += np.sum(self.fy_disc_disc, axis=0)
        self.fx_disc += np.sum(self.fx_wall_disc, axis=0)
        self.fy_disc += np.sum(self.fy_wall_disc, axis=0)

        # Specific to this simulation
        self.damper.calculate_forces()
        self.fx_disc[self.i_puck] += self.damper.fx
        self.fy_disc[self.i_puck] += self.damper.fy

        self.fy_disc[self.i_puck] += config.GRAVITY * self.m[self.i_puck]

    def update_positions(self):
        ax = self.fx_disc / self.m
        ay = self.fy_disc / self.m
        self.vx += config.CLOCK_PERIOD_SIM * ax
        self.vy += config.CLOCK_PERIOD_SIM * ay
        self.x += config.CLOCK_PERIOD_SIM * self.vx
        self.y += config.CLOCK_PERIOD_SIM * self.vy

        # Specific to this simulation
        # Wrap around
        if self.y[self.i_puck] < -self.r[self.i_puck]:
            y_old = self.y[self.i_puck]
            self.y[self.i_puck] = config.FIG_HEIGHT + self.r[self.i_puck]
            y_change = self.y[self.i_puck] - y_old
            self.damper.y_previous += y_change

        self.damper.x = self.x[self.i_puck]
        self.damper.y = self.y[self.i_puck]


@njit
def disc_disc_interaction_numba(
    col_tile,
    row_tile,
    fx_disc_disc,
    fy_disc_disc,
    k_disc_disc,
    r_disc_disc,
    x_col,
    x_row,
    y_col,
    y_row,
):
    # dx = (row_tile @ x[np.newaxis, :]) - (x[:, np.newaxis] @ col_tile)
    dx = (row_tile @ x_row) - (x_col @ col_tile)
    dy = (row_tile @ y_row) - (y_col @ col_tile)
    # dy = np.matmul(row_tile, y[np.newaxis, :]) - np.matmul(
    #     y[:, np.newaxis], col_tile
    # )
    epsilon = 1e-12
    distance = (dx**2 + dy**2) ** 0.5 + epsilon
    compression = r_disc_disc - distance
    compression = np.maximum(compression, 0)

    f_mag = k_disc_disc * compression
    f_norm = f_mag / distance
    fx_disc_disc += f_norm * dx
    fy_disc_disc += f_norm * dy
