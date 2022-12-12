import numpy as np
import matplotlib.patches as patches
import convert_svg

SVG_FILENAME = "grogu.svg"
SVG_IDS = ["head", "right_eye", "left_eye"]

# Palette from
# https://colorswall.com/palette/125797
GREEN = "#5c9c6d"  # rgb(92, 156, 109)
DARK = "#362f22"  # rgb(54, 47, 34)


class GroguViz:
    def __init__(self, ax):
        convert_svg.convert(SVG_FILENAME, SVG_IDS)

        self.head_path = np.load("head.npy")
        self.head_patch = ax.add_patch(
            patches.Polygon(
                self.head_path,
                facecolor=GREEN,
                edgecolor="none",
                zorder=1,
            )
        )

        self.right_eye_path = np.load("right_eye.npy")
        self.right_eye_patch = ax.add_patch(
            patches.Polygon(
                self.right_eye_path,
                facecolor=DARK,
                edgecolor="none",
                linewidth=1,
                joinstyle="round",
                zorder=2,
            )
        )

        self.left_eye_path = np.load("left_eye.npy")
        self.left_eye_patch = ax.add_patch(
            patches.Polygon(
                self.left_eye_path,
                facecolor=DARK,
                edgecolor="none",
                linewidth=1,
                joinstyle="round",
                zorder=2,
            )
        )

        self.x_center = 4
        self.y_center = 3

    def update(self, state):
        self.x = state["x"]
        self.y = state["y"]
        offset = np.array([[self.x, self.y]])

        self.head_patch.set_xy(self.head_path + offset)
        self.right_eye_patch.set_xy(self.right_eye_path + offset)
        self.left_eye_patch.set_xy(self.left_eye_path + offset)
