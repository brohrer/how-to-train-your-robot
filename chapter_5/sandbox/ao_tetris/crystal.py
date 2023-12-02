import numpy as np
from numba import njit
import config


class Crystal:
    def __init__(self, init_dict):
        self.name = init_dict["id"]
        self.n_atoms = init_dict["x"].size
        self.x = init_dict["x"]
        self.y = init_dict["y"]

        # If initial velocities aren't provided, initialize them to zero.
        try:
            self.vx = init_dict["vx"]
        except KeyError:
            self.vx = np.zeros(self.n_atoms)
        try:
            self.vy = init_dict["vy"]
        except KeyError:
            self.vy = np.zeros(self.n_atoms)

        # Default to a mass of 1, if no mass is provided.
        try:
            self.m = init_dict["m"]
        except KeyError:
            self.m = np.ones(self.n_atoms)

        self.r = init_dict["r"]
        # TODO ensure proper shape of k arrays
        self.k_external = init_dict["k_external"]
        self.k_internal = np.zeros((self.n_atoms, self.n_atoms))
        self.l_connection = np.zeros((self.n_atoms, self.n_atoms))

        self.bounding_box = {}
        self.update_bounding_box()

        # Handle the case where there are no internal connections provided.
        try:
            connections = init_dict["k_internal"]
            n_connections, _ = connections.shape
        except KeyError:
            n_connections = 0

        for i_conn in range(n_connections):
            i_atom, j_atom, k, length = tuple(connections[i_conn, :])
            i_atom = int(i_atom)
            j_atom = int(j_atom)
            self.k_internal[i_atom, j_atom] = k
            self.k_internal[j_atom, i_atom] = k
            self.l_connection[i_atom, j_atom] = length
            self.l_connection[j_atom, i_atom] = length

        # If an atom is free to move, it's 'free' value will be 1.
        # Otherwise 0.
        # If the value isn't specified, assume free.
        try:
            self.free = init_dict["free"]
        except KeyError:
            self.free = np.ones(self.n_atoms)

        self.fx = np.zeros(self.n_atoms)
        self.fy = np.zeros(self.n_atoms)
        self.fx_internal = np.zeros((self.n_atoms, self.n_atoms))
        self.fy_internal = np.zeros((self.n_atoms, self.n_atoms))
        self.row_tile = np.ones((self.n_atoms, 1))
        self.col_tile = np.ones((1, self.n_atoms))

    def start_step(self):
        self.fx = np.zeros(self.n_atoms)
        self.fy = np.zeros(self.n_atoms)
        self.fx_internal = np.zeros((self.n_atoms, self.n_atoms))
        self.fy_internal = np.zeros((self.n_atoms, self.n_atoms))
        self.update_bounding_box()

    def calculate_internal_forces(self):
        internal_interactions_numba(
            self.col_tile,
            self.row_tile,
            self.fx_internal,
            self.fy_internal,
            self.k_internal,
            self.l_connection,
            self.x[:, np.newaxis],
            self.x[np.newaxis, :],
            self.y[:, np.newaxis],
            self.y[np.newaxis, :],
        )

    def calculate_external_forces(self, crystal):
        # Check whether these two crystals have any chance of interaction
        # by comparing their bounding boxes.
        if self.is_close(crystal):
            external_interactions_numba(
                crystal.row_tile,
                self.col_tile,
                self.fx,
                crystal.fx,
                self.fy,
                crystal.fy,
                self.k_external[np.newaxis, :],
                crystal.k_external[:, np.newaxis],
                self.r[np.newaxis, :],
                crystal.r[:, np.newaxis],
                self.x[np.newaxis, :],
                crystal.x[:, np.newaxis],
                self.y[np.newaxis, :],
                crystal.y[:, np.newaxis],
            )

    def is_close(self, crystal):
        bb_a = self.bounding_box
        bb_b = crystal.bounding_box
        overlaps = True
        if (
            bb_a["x_min"] > bb_b["x_max"]
            or bb_b["x_min"] > bb_a["x_max"]
            or bb_a["y_min"] > bb_b["y_max"]
            or bb_b["y_min"] > bb_a["y_max"]
        ):
            overlaps = False
        return overlaps

    def update_bounding_box(self):
        self.bounding_box["x_min"] = np.min(self.x - self.r)
        self.bounding_box["x_max"] = np.max(self.x + self.r)
        self.bounding_box["y_min"] = np.min(self.y - self.r)
        self.bounding_box["y_max"] = np.max(self.y + self.r)

    def calculate_wall_forces(self, walls):
        wall_forces_numba(
            self.col_tile,
            np.ones((walls.count, 1)),
            self.fx,
            self.fy,
            self.k_external[np.newaxis, :],
            self.r,
            walls.x[:, np.newaxis],
            walls.x_n,
            self.x[np.newaxis, :],
            walls.y[:, np.newaxis],
            walls.y_n,
            self.y[np.newaxis, :],
        )

    def update_positions(self):
        update_positions_numba(
            self.x,
            self.y,
            self.vx,
            self.vy,
            self.m,
            self.free,
            self.fx,
            self.fy,
            self.fx_internal,
            self.fy_internal,
            config.CLOCK_PERIOD_SIM,
            config.SPEED_LIMIT,
        )

    def get_state(self):
        state = {
            "x": list(self.x),
            "y": list(self.y),
            "r": list(self.r),
        }
        return state


@njit
def internal_interactions_numba(
    col_tile,
    row_tile,
    fx_internal,
    fy_internal,
    k_internal,
    l_connection,
    x_col,
    x_row,
    y_col,
    y_row,
):
    dx = (row_tile @ x_row) - (x_col @ col_tile)
    dy = (row_tile @ y_row) - (y_col @ col_tile)
    epsilon = 1e-12
    distance = (dx**2 + dy**2) ** 0.5 + epsilon
    compression = l_connection - distance
    f_mag = k_internal * compression
    f_norm = f_mag / distance
    fx_internal += f_norm * dx
    fy_internal += f_norm * dy


@njit
def external_interactions_numba(
    row_tile_a,
    col_tile_b,
    fx_a,
    fx_b,
    fy_a,
    fy_b,
    k_a,
    k_b,
    r_a,
    r_b,
    x_a,
    x_b,
    y_a,
    y_b,
):
    epsilon = 1e-12
    dx = (row_tile_a @ x_a) - (x_b @ col_tile_b)
    dy = (row_tile_a @ y_a) - (y_b @ col_tile_b)
    r_ab = (row_tile_a @ r_a) - (r_b @ col_tile_b)
    k_ab = 1 / (
        row_tile_a @ (1 / (k_a + epsilon))
        + (1 / (k_b + epsilon)) @ col_tile_b
        + epsilon
    )
    distance = (dx**2 + dy**2) ** 0.5 + epsilon
    compression = r_ab - distance
    compression = np.maximum(compression, 0)
    f_mag = k_ab * compression
    f_norm = f_mag / distance

    fx_a += np.sum(f_norm * dx, axis=0)
    fx_b -= np.sum(f_norm * dx, axis=1)
    fy_a += np.sum(f_norm * dy, axis=0)
    fy_b -= np.sum(f_norm * dy, axis=1)


@njit
def wall_forces_numba(
    col_tile,
    row_tile,
    fx_atoms,
    fy_atoms,
    k_external,
    r_atoms,
    x_wall_col,
    x_n_wall,
    x_row,
    y_wall_col,
    y_n_wall,
    y_row,
):
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
    dx = (row_tile @ x_row) - (x_wall_col @ col_tile)
    dy = (row_tile @ y_row) - (y_wall_col @ col_tile)

    dx_n = dx * x_n_wall
    dy_n = dy * y_n_wall
    # Negative distance indicates that the center of the disc
    # is inside the wall.
    distance = dx_n + dy_n
    compression = r_atoms - distance
    compression = np.maximum(compression, 0)

    f_total = k_external * compression
    # Find the x- and y-components of the total force
    # with calculated sin (y_n / |dist|)
    # and cos (x_n / |dist|) terms.
    # Add a small nonzero term for numerical stability.
    epsilon = 1e-6
    fx_atoms_walls = f_total * x_n_wall / (np.abs(distance) + epsilon)
    fy_atoms_walls = f_total * y_n_wall / (np.abs(distance) + epsilon)
    fx_atoms += np.sum(fx_atoms_walls, axis=0)
    fy_atoms += np.sum(fy_atoms_walls, axis=0)


@njit
def update_positions_numba(
    x,
    y,
    vx,
    vy,
    m,
    free,
    fx,
    fy,
    fx_internal,
    fy_internal,
    CLOCK_PERIOD_SIM,
    SPEED_LIMIT,
):
    fx += np.sum(fx_internal, axis=0)
    fy += np.sum(fy_internal, axis=0)
    fx *= free
    fy *= free

    ax = fx / m
    ay = fy / m
    vx += CLOCK_PERIOD_SIM * ax
    vy += CLOCK_PERIOD_SIM * ay

    vx = np.maximum(vx, -SPEED_LIMIT)
    vx = np.minimum(vx, SPEED_LIMIT)
    vy = np.maximum(vy, -SPEED_LIMIT)
    vy = np.minimum(vy, SPEED_LIMIT)

    x += CLOCK_PERIOD_SIM * vx
    y += CLOCK_PERIOD_SIM * vy
