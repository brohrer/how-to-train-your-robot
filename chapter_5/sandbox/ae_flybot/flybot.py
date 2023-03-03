import config


class Flybot:
    def __init__(self):
        self.mass = config.BOT_MASS
        self.x = config.BOT_X
        self.y = config.BOT_Y
        self.vx = 0
        self.vy = 0
        self.fx = 0
        self.fy = 0

    def get_state(self):
        return {"x": self.x, "y": self.y, "vx": self.vx, "vy": self.vy}

    def update_position(self):
        ax = self.fx / self.mass
        ay = self.fy / self.mass
        self.vx += config.CLOCK_PERIOD_SIM * ax
        self.vy += config.CLOCK_PERIOD_SIM * ay
        self.x += config.CLOCK_PERIOD_SIM * self.vx
        self.y += config.CLOCK_PERIOD_SIM * self.vy

        self.fx = 0
        self.fy = 0
