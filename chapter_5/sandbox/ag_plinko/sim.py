import json
import time
import logging_setup
from pacemaker import Pacemaker
import config
from damper import Damper
from puck import Puck
import pegs
from wall import Wall


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

    while True:
        overtime = pacemaker.beat()
        if overtime > config.CLOCK_PERIOD_SIM:
            logger.error(json.dumps({"ts": time.time(), "overtime": overtime}))

        state = sim.step()
        ts = time.time()
        logger.debug(json.dumps({"ts": ts, "state": state}))

        steps_since_q_update += 1
        if steps_since_q_update >= steps_per_q_update:
            q.put((ts, state))
            steps_since_q_update = 0


class Simulation:
    def __init__(self):
        self.puck = Puck(
            mass=config.PUCK_MASS,
            radius=config.PUCK_RADIUS,
            stiffness=config.PUCK_STIFFNESS,
            x=config.PUCK_X,
            y=config.PUCK_Y,
        )
        self.peg_array = pegs.create_pegs()
        self.left_wall = Wall(x_left=0, y_left=0, x_right=0, y_right=1)
        self.right_wall = Wall(
            x_left=config.FIG_WIDTH,
            y_left=1,
            x_right=config.FIG_WIDTH,
            y_right=0,
        )
        self.damper = Damper(
            x=config.PUCK_X, y=config.PUCK_Y, damping=config.DAMPING
        )

    def step(self):
        self.calculate_forces()
        self.update_positions()
        state = self.get_state()
        return state

    def get_state(self):
        return {
            "puck": self.puck.get_state(),
            "pegs": pegs.get_state(self.peg_array),
            "damper": self.damper.get_state(),
        }

    def calculate_forces(self):
        self.puck.fx = 0
        self.puck.fy = 0

        for peg in self.peg_array:
            # The forces exerted *by* the peg on the puck.
            fx_on_puck, fy_on_puck = peg.calculate_collision_forces(self.puck)
            self.puck.fx += fx_on_puck
            self.puck.fy += fy_on_puck

        # Calculate forces due to hitting the side walls.
        # Distance will be negative if the puck is in contact with the wall.
        distance_left_wall = (
            self.left_wall.distance_to_point(self.puck.x, self.puck.y)
            - self.puck.radius
        )
        if distance_left_wall < 0:
            self.puck.fx += -1 * distance_left_wall * self.puck.stiffness

        distance_right_wall = (
            self.right_wall.distance_to_point(self.puck.x, self.puck.y)
            - self.puck.radius
        )
        if distance_right_wall < 0:
            self.puck.fx += distance_right_wall * self.puck.stiffness

        self.puck.fy += config.GRAVITY * self.puck.mass

        self.damper.calculate_forces()
        self.puck.fx += self.damper.fx
        self.puck.fy += self.damper.fy

    def update_positions(self):
        self.puck.update_position()
        # Wrap around
        if self.puck.y < -self.puck.radius:
            y_old = self.puck.y
            self.puck.y = config.FIG_HEIGHT + self.puck.radius
            y_change = self.puck.y - y_old
            self.damper.y_previous += y_change

        self.damper.x = self.puck.x
        self.damper.y = self.puck.y
