import numpy as np
import convert_svg

SVG_FILENAME = "spring.svg"
SVG_IDS = ["coil"]

# Palette from
# https://colorswall.com/palette/125797
GRAY = "#d3c1a5"  # rgb(211, 193, 165)
DARK = "#362f22"  # rgb(54, 47, 34)


class SpringViz:
    def __init__(self, ax):
        self.x_anchor = 0
        self.y_anchor = 0
        self.x_end = 0
        self.y_end = 0

        convert_svg.convert(SVG_FILENAME, SVG_IDS)
        self.coil_path = np.load("coil.npy")
        self.coil_length = np.max(self.coil_path[:, 1]) - np.min(
            self.coil_path[:, 1]
        )

        self.coil_line = ax.plot(
            self.coil_path[:, 0],
            self.coil_path[:, 1],
            color=DARK,
            linewidth=8,
            solid_joinstyle="round",
            solid_capstyle="round",
            zorder=0,
        )[0]

    def update(self, state):
        self.x_anchor = state["x_anchor"]
        self.y_anchor = state["y_anchor"]
        self.x_end = state["x_end"]
        self.y_end = state["y_end"]

        # scale length
        dx = self.x_end - self.x_anchor
        dy = self.y_end - self.y_anchor
        length = np.sqrt(dx**2 + dy**2)
        length_scale = length / self.coil_length
        path = np.copy(self.coil_path)
        path[:, 1] *= length_scale

        # rotate
        angle = np.arctan2(dy, dx) - np.pi / 2
        rotator = np.array(
            [[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]]
        )
        path = np.matmul(path, rotator)

        # translate
        anchor = np.array([self.x_anchor, self.y_anchor])
        path += anchor

        self.coil_line.set_xdata(path[:, 0])
        self.coil_line.set_ydata(path[:, 1])
