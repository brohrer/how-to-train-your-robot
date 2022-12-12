import json
import logging
import logging_setup
import time
from pacemaker import Pacemaker
from grogu import Grogu
from spring import Spring

CLOCK_FREQ = 1000  # Hertz
CLOCK_PERIOD = 1 / float(CLOCK_FREQ)


def run(q):
    logger = logging_setup.get_logger("sim", logging.INFO)
    sim = Simulation()
    pacemaker = Pacemaker(CLOCK_FREQ)

    while True:
        overtime = pacemaker.beat()
        if overtime > CLOCK_PERIOD:
            logger.error(json.dumps({"ts": time.time(), "overtime": overtime}))

        state = sim.step()
        ts = time.time()
        q.put((ts, state))
        logger.info(json.dumps({"ts": ts, "state": state}))


class Simulation:
    def __init__(self):
        self.grogu = Grogu(
            clock_period=CLOCK_PERIOD,
        )
        self.spring = Spring(
            clock_period=CLOCK_PERIOD,
            x_anchor=4,
            y_anchor=0.5,
            x_end=4,
            y_end=3,
            unstretched_length=2,
            stiffness=10,
        )

    def step(self):
        self.calculate_forces()
        self.update_positions()
        state = self.get_state()
        return state

    def get_state(self):
        return {
            "grogu": self.grogu.get_state(),
            "spring": self.spring.get_state(),
        }

    def calculate_forces(self):
        """
        Find the force of the spring acting on the bobblehead
        in the vertical direction
        """
        self.spring.calculate_forces()
        self.grogu.fx = self.spring.fx
        self.grogu.fy = self.spring.fy

    def update_positions(self):
        self.grogu.update_position()
        self.spring.x_end = self.grogu.x
        self.spring.y_end = self.grogu.y
