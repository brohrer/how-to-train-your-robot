import config


class Damper:
    def __init__(
        self,
        x=0,
        y=0,
        damping=1,
    ):
        self.damping = damping
        self.x = x
        self.y = y
        self.x_previous = self.x
        self.y_previous = self.y
        self.vx = 0
        self.vy = 0

        self.fx = 0
        self.fy = 0

    def get_state(self):
        return {
            "x": self.x,
            "y": self.y,
            "vx": self.vx,
            "vy": self.vy,
        }

    def calculate_forces(self):
        self.vx = (self.x - self.x_previous) / config.CLOCK_PERIOD_SIM
        self.vy = (self.y - self.y_previous) / config.CLOCK_PERIOD_SIM
        self.fx = -self.vx * self.damping
        self.fy = -self.vy * self.damping

        self.x_previous = self.x
        self.y_previous = self.y
