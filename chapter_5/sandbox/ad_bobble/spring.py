import numpy as np


class Spring:
    def __init__(
        self,
        clock_period=0.001,
        x_anchor=0,
        y_anchor=0,
        x_end=1,
        y_end=1,
        unstretched_length=1,
        stiffness=1,
    ):
        # Things that don't change
        self.clock_period = clock_period
        self.unstretched_length = unstretched_length
        self.stiffness = stiffness

        # Things that do change
        self.x_anchor = x_anchor
        self.y_anchor = y_anchor
        self.x_end = x_end
        self.y_end = y_end
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
        length = np.sqrt(dx**2 + dy**2)
        deviation = length - self.unstretched_length
        force = -deviation * self.stiffness
        self.fx = force * dx / length
        self.fy = force * dy / length
