import json
import logging_setup
import time

# import numpy as np
import matplotlib.pyplot as plt

# import matplotlib.patches as patches
from pacemaker import Pacemaker
from flybot_viz import BotViz
from ground_viz import GroundViz
import colors
import config

FIG_HEIGHT = 6  # inches
FIG_WIDTH = 8  # inches


def run(q):
    logger = logging_setup.get_logger("viz", config.LOGGING_LEVEL_VIZ)
    frame = Frame()
    clock_period = 1 / float(config.CLOCK_FREQ_VIZ)
    pacemaker = Pacemaker(config.CLOCK_FREQ_VIZ)
    ts = None
    state = None

    while True:
        overtime = pacemaker.beat()
        if overtime > clock_period:
            logger.error(json.dumps({"ts": time.time(), "overtime": overtime}))

            # If the visualization is running behind
            # skip this frame to help catch up.
            continue

        while not q.empty():
            ts, state = q.get()

        logger.debug(json.dumps({"ts": ts, "state": state}))
        frame.update(state)


class Frame:
    def __init__(self):
        self.ax = self.draw_frame()

        self.bot = BotViz(self.ax)
        self.ground = GroundViz(self.ax)

        plt.ion()
        plt.show()

    def draw_frame(self):

        self.fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
        ax = self.fig.add_axes((0, 0, 1, 1))
        ax.set_facecolor(colors.LIGHT_BROWN)
        ax.set_xlim(0, FIG_WIDTH)
        ax.set_ylim(0, FIG_HEIGHT)

        return ax

    def update(self, state):
        if state is None:
            return

        self.bot.update(state["bot"])
        self.ground.update(state["ground"])

        self.fig.canvas.flush_events()
