import json
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import logging_setup
from pacemaker import Pacemaker
import config


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
        self.pegs_drawn = False

        self.fig = plt.figure(
            figsize=(
                config.FIG_WIDTH * config.FIG_SCALE,
                config.FIG_HEIGHT * config.FIG_SCALE,
            )
        )
        self.ax = self.fig.add_axes((0, 0, 1, 1))
        self.ax.set_facecolor(config.BOARD_COLOR)
        self.ax.set_xlim(0, config.FIG_WIDTH)
        self.ax.set_ylim(0, config.FIG_HEIGHT)

        t = np.linspace(0, 2 * np.pi, 37)
        x = np.cos(t) * config.PUCK_RADIUS
        y = np.sin(t) * config.PUCK_RADIUS
        self.puck_path = np.concatenate(
            (x[:, np.newaxis], y[:, np.newaxis]), axis=1
        )
        self.puck_patch = self.ax.add_patch(
            patches.Polygon(
                self.puck_path,
                facecolor=config.PUCK_COLOR,
                edgecolor="none",
                zorder=1,
            )
        )
        plt.ion()
        plt.show()

    def draw_pegs(self, pegs_state):
        t = np.linspace(0, 2 * np.pi, 17)
        x = np.cos(t) * config.PEG_RADIUS
        y = np.sin(t) * config.PEG_RADIUS
        peg_path = np.concatenate((x[:, np.newaxis], y[:, np.newaxis]), axis=1)

        for key, peg_state in pegs_state.items():
            self.ax.add_patch(
                patches.Polygon(
                    peg_path + np.array([[peg_state["x"], peg_state["y"]]]),
                    facecolor=config.PEG_COLOR,
                    edgecolor="none",
                    zorder=2,
                )
            )

        self.pegs_drawn = True
        return

    def update(self, state):
        if state is None:
            return

        if not self.pegs_drawn:
            self.draw_pegs(state["pegs"])

        self.x = state["puck"]["x"]
        self.y = state["puck"]["y"]
        offset = np.array([[self.x, self.y]])
        self.puck_patch.set_xy(self.puck_path + offset)

        self.fig.canvas.flush_events()
