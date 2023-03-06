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

    i_over = 0.0
    i_total = 0.0
    while True:
        overtime = pacemaker.beat()
        if overtime > clock_period:
            logger.error(json.dumps({"ts": time.time(), "overtime": overtime}))

            # If the visualization is running behind
            # skip this frame to help catch up.
            continue

        i_total += 1
        if overtime > config.CLOCK_PERIOD_SIM * 0.5:
            i_over += 1
            print(
                f"viz over {overtime / config.CLOCK_PERIOD_SIM}"
                + f"  {i_over / i_total}"
            )

        while not q.empty():
            ts, state = q.get()

        logger.debug(json.dumps({"ts": ts, "state": state}))
        frame.update(state)


class Frame:
    def __init__(self):
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

        slope_path = np.array(
            [
                [0, 0],
                [0, config.FLOOR_OFFSET],
                [config.FIG_WIDTH, config.FLOOR_OFFSET + config.FLOOR_DROP],
                [config.FIG_WIDTH, 0],
            ]
        )
        self.ax.add_patch(
            patches.Polygon(
                slope_path,
                facecolor=config.GROUND_COLOR,
                edgecolor="none",
                zorder=0,
            )
        )

        t = np.linspace(0, 2 * np.pi, 37)
        x = np.cos(t)
        y = np.sin(t)
        self.disc_path = np.concatenate(
            (x[:, np.newaxis], y[:, np.newaxis]), axis=1
        )
        self.peg_path = self.disc_path * config.PEG_RADIUS

        for f in config.FEATURES:
            self.ax.add_patch(
                patches.Polygon(
                    self.disc_path * f[2] + np.array([f[0], f[1]]),
                    facecolor=config.GROUND_COLOR,
                    edgecolor="none",
                    zorder=0,
                )
            )

        plt.ion()
        plt.show()

        self.pegs_created = False

    def update(self, state):
        if state is None:
            return

        if not self.pegs_created:
            self.draw_pegs(state)
            self.pegs_created = True

        self.update_pegs(state)
        self.fig.canvas.flush_events()

    def draw_pegs(self, state):
        pegs_state = state["pegs"]

        self.peg_patches = []
        for key, peg_state in pegs_state.items():
            peg_patch = self.ax.add_patch(
                patches.Polygon(
                    self.peg_path
                    + np.array([[peg_state["x"], peg_state["y"]]]),
                    facecolor=config.PEG_COLOR,
                    edgecolor="none",
                    zorder=2,
                )
            )
            self.peg_patches.append(peg_patch)

    def update_pegs(self, state):
        pegs_state = state["pegs"]
        for i_peg, peg_state in enumerate(pegs_state.values()):
            new_path = self.peg_path + np.array(
                [[peg_state["x"], peg_state["y"]]]
            )
            self.peg_patches[i_peg].set_xy(new_path)
