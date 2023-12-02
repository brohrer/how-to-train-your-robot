import json
import os

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tools.logging_setup as logging_setup
from tools.pacemaker import Pacemaker
import config


def run(sim_viz_state_q, run_viz_alive_q, viz_run_alive_q):
    logger = logging_setup.get_logger("viz", config.LOGGING_LEVEL_VIZ)
    frame = Frame()
    clock_period = 1 / float(config.CLOCK_FREQ_VIZ)
    pacemaker = Pacemaker(config.CLOCK_FREQ_VIZ)
    n_alive_check = int(config.CLOCK_FREQ_VIZ / config.ALIVE_CHECK_FREQ)
    i_alive_check = 0
    ts = None
    state = None

    while True:
        overtime = pacemaker.beat()

        # Send a heartbeat from this process to the parent runner process,
        # reassuring it that everything here is okie dokie.
        viz_run_alive_q.put(True)

        # Watch for a heartbeat from the parent runner process.
        # If it is not found, then shut down this process too.
        i_alive_check += 1

        if i_alive_check == n_alive_check:
            runner_is_alive = False
            while not run_viz_alive_q.empty():
                runner_is_alive = run_viz_alive_q.get()
            if not runner_is_alive:
                print("Runner process has shut down.")
                print("Shutting down visualization process.")
                # sys.exit()
                os._exit(os.EX_OK)
            else:
                i_alive_check = 0

        if overtime > clock_period:
            logger.warning(
                json.dumps({"ts": time.time(), "overtime": overtime})
            )

            # If the visualization is running behind
            # skip this frame to help catch up.
            continue

        while not sim_viz_state_q.empty():
            ts, state = sim_viz_state_q.get()

        logger.debug(json.dumps({"ts": ts, "state": state}))
        frame.update(state)


class Frame:
    def __init__(self):
        self.fig = plt.figure(
            figsize=(config.FIG_WIDTH, config.FIG_HEIGHT),
            num="Simulation",
        )
        self.ax = self.fig.add_axes((0, 0, 1, 1))
        self.ax.set_facecolor(config.BACKGROUND_COLOR)
        self.ax.set_xlim(0, config.WORLD_WIDTH)
        self.ax.set_ylim(0, config.WORLD_HEIGHT)

        t = np.linspace(0, 2 * np.pi, 37)
        x = np.cos(t)
        y = np.sin(t)
        self.atom_path = np.concatenate(
            (x[:, np.newaxis], y[:, np.newaxis]), axis=1
        )

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
        self.bodies = {}
        for body_id, atom_states in state.items():
            atom_patches = []
            x = atom_states["x"]
            y = atom_states["y"]
            r = atom_states["r"]
            for i in range(len(x)):
                atom_patch = self.ax.add_patch(
                    patches.Polygon(
                        self.atom_path * r[i] + np.array([x[i], y[i]]),
                        facecolor=config.BODIES[body_id]["color"],
                        # facecolor=config.BODY_COLOR[body_id],
                        edgecolor="none",
                        zorder=2,
                    )
                )
                atom_patches.append(atom_patch)
            self.bodies[body_id] = atom_patches

    def update_atoms(self, state):
        for body_id, atom_states in state.items():
            atom_patches = self.bodies[body_id]
            x = atom_states["x"]
            y = atom_states["y"]
            r = atom_states["r"]
            for i in range(len(x)):
                new_path = self.atom_path * r[i] + np.array([x[i], y[i]])
                atom_patches[i].set_xy(new_path)
