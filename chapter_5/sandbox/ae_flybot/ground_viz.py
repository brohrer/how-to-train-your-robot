import numpy as np
import matplotlib.patches as patches
import colors


class GroundViz:
    def __init__(self, ax):
        self.x = 0
        self.y = 0

        self.x_min = 0
        self.x_max = ax.get_xlim()[1]
        terrain_path = np.array(
            [
                [self.x_min, 0],
                [self.x_min, 1],
                [self.x_max, 1],
                [self.x_max, 0],
            ]
        )
        self.terrain_patch = ax.add_patch(
            patches.Polygon(
                terrain_path,
                facecolor=colors.BROWN,
                edgecolor="none",
                linewidth=0.5,
                zorder=2,
            )
        )

    def update(self, state):
        terrain = np.array(state["terrain"])
        x = np.linspace(self.x_min, self.x_max, terrain.size)
        path = np.concatenate(
            (x[:, np.newaxis], terrain[:, np.newaxis]), axis=1
        )
        path = np.concatenate(
            (path, np.array([[self.x_max, 0], [self.x_min, 0]])), axis=0
        )

        self.terrain_patch.set_xy(path)
