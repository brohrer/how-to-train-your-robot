import json
import logging_setup
import time
from pacemaker import Pacemaker
import config
from flybot import Flybot
from ground import Ground
from damper import Damper
from spring import Spring


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
        self.bot = Flybot()
        self.ground = Ground()
        self.spring = Spring()
        self.damper = Damper()

    def step(self):
        self.calculate_forces()
        self.update_positions()
        state = self.get_state()
        return state

    def get_state(self):
        return {
            "bot": self.bot.get_state(),
            "ground": self.ground.get_state(),
            "damper": self.damper.get_state(),
            "spring": self.spring.get_state(),
        }

    def calculate_forces(self):
        """
        Find the force of the spring acting on the bobblehead
        in the vertical direction
        """
        self.bot.fx = 0
        self.bot.fy = 0

        self.damper.calculate_forces()
        self.bot.fx += self.damper.fx
        self.bot.fy += self.damper.fy

        self.spring.calculate_forces()
        self.bot.fx += self.spring.fx
        self.bot.fy += self.spring.fy

    def update_positions(self):
        self.bot.update_position()
        self.ground.update_position()

        self.damper.x_end = self.bot.x
        self.damper.y_end = self.bot.y
        self.damper.x_anchor = self.ground.x
        self.damper.y_anchor = self.ground.y

        self.spring.x_end = self.bot.x
        self.spring.y_end = self.bot.y
        self.spring.x_anchor = self.ground.x
        self.spring.y_anchor = self.ground.y
