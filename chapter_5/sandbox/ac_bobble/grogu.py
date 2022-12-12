class Grogu:
    def __init__(
        self,
        clock_period=1,
        mass=0.2,
        x=4,
        y=3.3,
        vx=0,
        vy=0,
        fx=0,
        fy=0,
    ):
        # Things that don't change
        self.clock_period = clock_period
        self.mass = mass

        # Things that change
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.fx = fx
        self.fy = fy

    def get_state(self):
        return {"x": self.x, "y": self.y, "vx": self.vx, "vy": self.vy}

    def update_position(self):
        ax = self.fx / self.mass
        ay = self.fy / self.mass
        self.vx += self.clock_period * ax
        self.vy += self.clock_period * ay
        self.x += self.clock_period * self.vx
        self.y += self.clock_period * self.vy

        self.fx = 0
        self.fy = 0
