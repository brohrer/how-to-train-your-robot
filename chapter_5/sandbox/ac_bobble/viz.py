import json
import logging
import logging_setup
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pacemaker import Pacemaker
from grogu_viz import GroguViz
from spring_viz import SpringViz

FIG_HEIGHT = 6  # inches
FIG_WIDTH = 8  # inches
CLOCK_FREQ = 48  # Hertz
LOGGING_LEVEL = logging.DEBUG

# Palette from
# https://colorswall.com/palette/125797
YELLOW = "#fac73b"  # rgb(250, 199, 59)
TAN = "#f8db91"  # rgb(248, 219, 145)
BROWN = "#815f03"  # rgb(129, 95, 3)
GRAY = "#d3c1a5"  # rgb(211, 193, 165)


def run(q):
    logger = logging_setup.get_logger("viz", LOGGING_LEVEL)
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
        self.ax = self.draw_frame()

        self.grogu = GroguViz(self.ax)
        self.spring = SpringViz(self.ax)

        plt.ion()
        plt.show()

    def draw_frame(self):
        plains_height = FIG_HEIGHT * 0.65
        hills_height = FIG_HEIGHT * 0.1

        self.fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
        ax = self.fig.add_axes((0, 0, 1, 1))
        ax.set_facecolor(GRAY)
        ax.set_xlim(0, FIG_WIDTH)
        ax.set_ylim(0, FIG_HEIGHT)

        plains_path = np.array(
            [
                [0, 0],
                [FIG_WIDTH, 0],
                [FIG_WIDTH, plains_height],
                [0, plains_height],
            ]
        )
        ax.add_patch(
            patches.Polygon(
                plains_path,
                facecolor=TAN,
                edgecolor="none",
                zorder=0,
            )
        )

        hills_path = np.array(
            [
                [0, 0],
                [1, 0],
                [1, 0.7],
                [0.9, 0.2],
                [0.87, 0.3],
                [0.8, 0.05],
                [0.4, 0.05],
                [0.3, 0.6],
                [0.2, 0.4],
                [0.1, 1],
                [0, 0.8],
            ]
        ) * np.array([[FIG_WIDTH, hills_height]]) + np.array(
            [[0, plains_height]]
        )
        ax.add_patch(
            patches.Polygon(
                hills_path,
                facecolor=BROWN,
                edgecolor="none",
                zorder=0,
            )
        )

        t = np.linspace(0, 2 * np.pi, 72)
        x = np.cos(t)
        y = np.sin(t)
        circle_path = np.concatenate(
            (x[:, np.newaxis], y[:, np.newaxis]), axis=1
        )

        r1 = FIG_HEIGHT * 0.1
        x1 = FIG_WIDTH * 0.7
        y1 = FIG_HEIGHT * 0.8
        sun1_path = circle_path * r1 + np.array([[x1, y1]])
        ax.add_patch(
            patches.Polygon(
                sun1_path,
                facecolor=YELLOW,
                edgecolor="none",
                zorder=0,
            )
        )

        r2 = FIG_HEIGHT * 0.04
        x2 = FIG_WIDTH * 0.85
        y2 = FIG_HEIGHT * 0.75
        sun2_path = circle_path * r2 + np.array([[x2, y2]])
        ax.add_patch(
            patches.Polygon(
                sun2_path,
                facecolor=TAN,
                edgecolor="none",
                zorder=0,
            )
        )
        return ax

    def update(self, state):
        if state is None:
            return

        self.grogu.update(state["grogu"])
        self.spring.update(state["spring"])

        self.fig.canvas.flush_events()
