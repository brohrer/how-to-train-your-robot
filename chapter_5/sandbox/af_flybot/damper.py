import config


class Damper:
    def __init__(self):
        self.damping = config.DAMPING

        self.x_anchor = config.GROUND_X
        self.y_anchor = config.GROUND_Y
        self.x_end = config.BOT_X
        self.y_end = config.BOT_Y

        self.previous_length = self.get_length()
        self.fx = 0
        self.fy = 0

    def get_state(self):
        return {
            "x_anchor": self.x_anchor,
            "y_anchor": self.y_anchor,
            "x_end": self.x_end,
            "y_end": self.y_end,
        }

    def get_length(self):
        dx = self.x_end - self.x_anchor
        dy = self.y_end - self.y_anchor
        return (dx**2 + dy**2) ** 0.5

    def calculate_forces(self):
        dx = self.x_end - self.x_anchor
        dy = self.y_end - self.y_anchor
        length = self.get_length()
        length_change_rate = (
            length - self.previous_length
        ) / config.CLOCK_PERIOD_SIM
        force = -length_change_rate * self.damping
        self.fx = force * dx / length
        self.fy = force * dy / length

        self.previous_length = length
