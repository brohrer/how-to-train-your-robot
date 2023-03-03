import random
import numpy as np
import config


class Ground:
    def __init__(self):
        self.x = config.GROUND_X
        self.ground_baseline = config.GROUND_Y
        self.y = self.ground_baseline
        self.vx = 0
        self.vy = 0

        self.terrain_size = 1000
        self.i_start = int(self.terrain_size / 2)
        self.i_end = self.i_start + self.terrain_size
        self.i_current = self.terrain_size
        self.terrain = np.ones(self.terrain_size * 2) * self.ground_baseline
        self.step_width = int(self.terrain_size / 4)

    def get_state(self):
        return {
            "x": self.x,
            "y": self.y,
            "vx": self.vx,
            "vy": self.vy,
            "terrain": list(
                self.terrain[self.i_start : self.i_end]  # noqa: E203
            ),
        }

    def update_position(self):
        # Shift by one element
        self.terrain = np.roll(self.terrain, 1)
        self.terrain[0] = self.ground_baseline

        if random.random() < config.INCIDENCE:
            delta_y = random.gauss(0, config.SCALE)
            self.terrain[: self.step_width] += delta_y

        y_new = self.terrain[self.i_current]

        self.vy += (y_new - self.y) / config.CLOCK_PERIOD_SIM
        self.y = y_new
