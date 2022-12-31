import config


class Spring:
    def __init__(self):
        # Things that don't change
        self.unstretched_length = config.UNSTRETECHED_LENGTH
        self.stiffness = config.STIFFNESS

        # Things that do change
        self.x_anchor = config.GROUND_X
        self.y_anchor = config.GROUND_Y
        self.x_end = config.BOT_X
        self.y_end = config.BOT_Y
        self.fx = 0
        self.fy = 0

    def get_state(self):
        return {
            "x_anchor": self.x_anchor,
            "y_anchor": self.y_anchor,
            "x_end": self.x_end,
            "y_end": self.y_end,
        }

    def calculate_forces(self):
        dx = self.x_end - self.x_anchor
        dy = self.y_end - self.y_anchor
        length = (dx**2 + dy**2) ** 0.5
        deviation = length - self.unstretched_length
        force = -deviation * self.stiffness
        self.fx = force * dx / length
        self.fy = force * dy / length
