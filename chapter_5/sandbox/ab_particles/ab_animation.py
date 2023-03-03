import json
import logging
import logging_setup
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pacemaker import Pacemaker

FIG_WIDTH = 8  # inches
FIG_HEIGHT = 5  # inches
RADIUS = 0.2  # inches
CLOCK_FREQ = 48  # Hertz
LOGGING_LEVEL = logging.DEBUG

BILLIARD = "#155843"
DEEP_BLUE = "#08415C"
AQUA = "#388697"
SKY = "#7BD1DA"
RUBY = "#CC2936"
IVORY = "#FFFFF0"


def run(q):
    logger = logging_setup.get_logger("ani", LOGGING_LEVEL)
    frame = Frame()
    clock_period = 1 / float(CLOCK_FREQ)
    pacemaker = Pacemaker(CLOCK_FREQ)
    ts = None
    state = None

    while True:
        overtime = pacemaker.beat()
        if overtime > clock_period:
            logger.error(json.dumps({"ts": time.time(), "overtime": overtime}))

        while not q.empty():
            ts, state = q.get()

        logger.debug(json.dumps({"ts": ts, "state": state}))
        frame.update(state)


class Frame:
    def __init__(self):
        self.fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
        self.ax = self.fig.add_axes((0, 0, 1, 1))
        self.ax.set_facecolor(BILLIARD)
        self.ax.set_xlim(0, FIG_WIDTH)
        self.ax.set_ylim(0, FIG_HEIGHT)

        self.particle = ParticleArt(self.ax)

        plt.ion()
        plt.show()

    def update(self, state):
        if state is None:
            return

        particle_state = state["particle"]
        self.particle.update(particle_state)

        self.fig.canvas.flush_events()


class ParticleArt:
    def __init__(self, ax):
        self.x_center = 0
        self.y_center = 0

        n_points = 72
        angle = np.linspace(0, 2 * np.pi, n_points)
        self.xs = RADIUS * np.cos(angle)[:, np.newaxis]
        self.ys = RADIUS * np.sin(angle)[:, np.newaxis]
        path = np.concatenate((self.xs, self.ys), axis=1)
        self.patch = ax.add_patch(
            patches.Polygon(
                path,
                facecolor=IVORY,
                edgecolor="none",
                linewidth=1,
                joinstyle="round",
            )
        )

    def update(self, state):
        self.x_center = state["x"]
        self.y_center = state["y"]

        path = np.concatenate(
            (self.xs + self.x_center, self.ys + self.y_center), axis=1
        )
        self.patch.set_xy(path)
