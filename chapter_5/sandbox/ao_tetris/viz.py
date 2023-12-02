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
            # print(
            #     f"viz over {overtime / config.CLOCK_PERIOD_SIM}"
            #     + f"  {i_over / i_total}"
            # )
            print(
                f"   viz over {int(100 * overtime / config.CLOCK_PERIOD_SIM)}%"
                + " this iteration"
                + f"  {100 * i_over / i_total:.2f}% cumulative"
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
        self.ax.set_facecolor(config.BACKGROUND_COLOR)
        self.ax.set_xlim(0, config.FIG_WIDTH)
        self.ax.set_ylim(0, config.FIG_HEIGHT)

        t = np.linspace(0, 2 * np.pi, 37)
        x = np.cos(t)
        y = np.sin(t)
        self.disc_path = np.concatenate(
            (x[:, np.newaxis], y[:, np.newaxis]), axis=1
        )
        self.atom_path = self.disc_path

        plt.ion()
        plt.show()

        self.atoms_created = False

    def update(self, state):
        if state is None:
            return

        if not self.atoms_created:
            self.draw_atoms(state)
            self.atoms_created = True

        self.update_atoms(state)
        self.fig.canvas.flush_events()

    def draw_atoms(self, state):
        self.crystals = {}
        for crystal_id, atom_states in state.items():
            atom_patches = []
            x = atom_states["x"]
            y = atom_states["y"]
            r = atom_states["r"]
            for i in range(len(x)):
                atom_patch = self.ax.add_patch(
                    patches.Polygon(
                        self.atom_path * r[i] + np.array([x[i], y[i]]),
                        facecolor=config.CRYSTAL_COLOR[crystal_id],
                        edgecolor="none",
                        zorder=2,
                    )
                )
                atom_patches.append(atom_patch)
            self.crystals[crystal_id] = atom_patches

    def update_atoms(self, state):
        for crystal_id, atom_states in state.items():
            atom_patches = self.crystals[crystal_id]
            x = atom_states["x"]
            y = atom_states["y"]
            r = atom_states["r"]
            for i in range(len(x)):
                new_path = self.atom_path * r[i] + np.array([x[i], y[i]])
                atom_patches[i].set_xy(new_path)
