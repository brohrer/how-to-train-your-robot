import config


class Wall:
    """
    A half-plane
    """

    def __init__(
        self,
        x_left=0,
        y_left=0,
        x_right=0,
        y_right=0,
    ):
        """
        Initialize with two points on the line.
        Imagine you are looking at the wall.
        One point will be on the left (x_left, y_left)
        and the other will be on the right (x_right, y_right).
        """
        # An arbitrary point on the line
        self.x = x_left
        self.y = y_left

        # A unit vector normal to the surface of the wall
        # pointing away from the wall.
        self.x_normal, self.y_normal = self.calculate_normal(
            x_left, y_left, x_right, y_right
        )

    def get_state(self):
        return {
            "x": self.x,
            "y": self.y,
            "x_normal": self.x_normal,
            "y_normal": self.y_normal,
        }

    def calculate_normal(self, x_left, y_left, x_right, y_right):
        dist_lr = ((x_left - x_right) ** 2 + (y_left - y_right) ** 2) ** 0.5
        epsilon = 1e-12
        if dist_lr < epsilon:
            raise ValueError("Left and right points need to be further apart")

        x_normal = (y_right - y_left) / dist_lr
        y_normal = (x_left - x_right) / dist_lr
        return (x_normal, y_normal)

    def distance_to_point(self, x, y):
        """
        Calculate the distance from the wall to any point (x, y)
        x and y can also be Numpy arrays of equal sizes, if you
        want to quickly calculate the distance to many points at once.

        Taken from
        https://en.wikipedia.org/w/index.php?title=Distance_from_a_point_to_a_line
        and modfied to the form
        d = (x - x1) * x_normal + (y - y1) * y_normal
        where (x1, y1) is any point on the line.

        This is a signed distance.
        A positive value indicates distance away from the wall.
        A negative value indicates distance *into* the wall.
        """
        return (x - self.x) * self.x_normal + (y - self.y) * self.y_normal

    def update_position(self):
        ax = self.fx / self.mass
        ay = self.fy / self.mass
        self.vx += config.CLOCK_PERIOD_SIM * ax
        self.vy += config.CLOCK_PERIOD_SIM * ay
        self.x += config.CLOCK_PERIOD_SIM * self.vx
        self.y += config.CLOCK_PERIOD_SIM * self.vy

        self.fx = 0
        self.fy = 0
