import numpy as np


class Walls:
    def __init__(self, sliding_friction=None, inelasticity=None):
        self.x = np.zeros(0)
        self.y = np.zeros(0)
        self.x_n = np.zeros(0)
        self.y_n = np.zeros(0)
        self.count = 0

        # Default to a sliding friction coefficient if none is provided.
        if sliding_friction is not None:
            self.sliding_friction = sliding_friction
        else:
            self.sliding_friction = 0.3

        # Default to an inelasticity coefficient if none is provided.
        if inelasticity is not None:
            self.inelasticity = inelasticity
        else:
            self.inelasticity = 0.2

    def add_wall(self, wall_init):
        # def add_wall(self, x_left, y_left, x_right, y_right):
        """
        Initialize with two points on the line.
        Imagine you are looking at the wall.
        One point will be on the left (x_left, y_left)
        and the other will be on the right (x_right, y_right).
        """
        x_left = wall_init["x_left"]
        x_right = wall_init["x_right"]
        y_left = wall_init["y_left"]
        y_right = wall_init["y_right"]

        # A unit vector normal to the surface of the wall
        # pointing away from the wall.
        x_normal, y_normal = self.calculate_wall_normal(
            x_left, y_left, x_right, y_right
        )
        # An arbitrary point on the line
        self.x = np.concatenate((self.x, np.array([x_left])))
        self.y = np.concatenate((self.y, np.array([y_left])))
        self.x_n = np.concatenate((self.x_n, np.array([x_normal])))
        self.y_n = np.concatenate((self.y_n, np.array([y_normal])))
        self.count += 1
        return

    def calculate_wall_normal(self, x_left, y_left, x_right, y_right):
        dist_lr = ((x_left - x_right) ** 2 + (y_left - y_right) ** 2) ** 0.5
        epsilon = 1e-12
        if dist_lr < epsilon:
            raise ValueError("Left and right points need to be further apart")

        x_normal = (y_right - y_left) / dist_lr
        y_normal = (x_left - x_right) / dist_lr
        return (x_normal, y_normal)
