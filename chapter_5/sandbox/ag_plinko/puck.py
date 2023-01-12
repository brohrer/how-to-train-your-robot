import config


class Puck:
    def __init__(
        self,
        mass=1,
        radius=1,
        stiffness=1,
        x=0,
        y=0,
        vx=0,
        vy=0,
    ):
        self.mass = mass
        self.radius = radius
        self.stiffness = stiffness
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
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
