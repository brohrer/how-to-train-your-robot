import json
import logging
import logging_setup
import time
import numpy as np
from pacemaker import Pacemaker

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
        self.particle = Particle()
        self.left_wall = 0
        self.right_wall = 8
        self.bottom_wall = 0
        self.top_wall = 5

    def step(self):
        self.calculate_forces()
        self.update_positions()
        state = self.get_state()
        return state

    def get_state(self):
        return {"particle": self.particle.get_state()}

    def calculate_forces(self):
        """
        Calculate any forces between the particle and each of the walls
        """
        # Distance from the wall to the particle.
        # Negative distance indicates contact and compression of the particle.
        d_left = (self.particle.x - self.particle.radius) - self.left_wall
        compression = -np.minimum(d_left, 0)
        force = compression * self.particle.stiffness
        self.particle.fx += force

        d_right = self.right_wall - (self.particle.x + self.particle.radius)
        compression = -np.minimum(d_right, 0)
        force = compression * self.particle.stiffness
        self.particle.fx += -force

        d_bottom = (self.particle.y - self.particle.radius) - self.bottom_wall
        compression = -np.minimum(d_bottom, 0)
        force = compression * self.particle.stiffness
        self.particle.fy += force

        d_top = self.top_wall - (self.particle.y + self.particle.radius)
        compression = -np.minimum(d_top, 0)
        force = compression * self.particle.stiffness
        self.particle.fy += -force

    def update_positions(self):
        self.particle.update_position()


class Particle:
    def __init__(
        self,
        mass=1,
        radius=0.1,
        stiffness=1000,
        x=0,
        y=0,
        vx=0,
        vy=0,
        # ax=0,
        # ay=0,
        fx=0,
        fy=0,
    ):
        # Things that don't change
        self.mass = mass
        self.radius = radius
        self.stiffness = stiffness

        # Things that change
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        # self.ax = ax
        # self.ay = ay
        self.fx = fx
        self.fy = fy

    def get_state(self):
        return {"x": self.x, "y": self.y, "vx": self.vx, "vy": self.vy}

    def update_position(self):
        # ax_new = self.fx / self.mass
        # ay_new = self.fy / self.mass
        # vx_new = self.vx + CLOCK_PERIOD * (self.ax + ax_new) / 2
        # vy_new = self.vy + CLOCK_PERIOD * (self.ay + ay_new) / 2
        # self.x = self.x + CLOCK_PERIOD * (self.vx + vx_new) / 2
        # self.y = self.y + CLOCK_PERIOD * (self.vy + vy_new) / 2
        ax = self.fx / self.mass
        ay = self.fy / self.mass
        self.vx += CLOCK_PERIOD * ax
        self.vy += CLOCK_PERIOD * ay
        self.x += CLOCK_PERIOD * self.vx
        self.y += CLOCK_PERIOD * self.vy

        self.fx = 0
        self.fy = 0
        # self.ax = ax_new
        # self.ay = ay_new
        # self.vx = vx_new
        # self.vy = vy_new
