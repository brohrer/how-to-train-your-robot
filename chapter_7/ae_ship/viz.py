import json
import os

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tools.logging_setup as logging_setup
from tools.pacemaker import Pacemaker
import config


def run(sim_viz_info_q, run_viz_alive_q, viz_run_alive_q):
    logger = logging_setup.get_logger("viz", config.LOGGING_LEVEL_VIZ)
    frame = Frame()
    clock_period = 1 / float(config.CLOCK_FREQ_VIZ)
    pacemaker = Pacemaker(config.CLOCK_FREQ_VIZ)
    n_alive_check = int(config.CLOCK_FREQ_VIZ / config.ALIVE_CHECK_FREQ)
    i_alive_check = 0
    ts = None
    viz_info = None

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

        while not sim_viz_info_q.empty():
            ts, viz_info = sim_viz_info_q.get()

        logger.debug(json.dumps({"ts": ts, "viz_info": viz_info}))
        frame.update(viz_info)


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

        plt.ion()
        plt.show()

        self.body_patches = {}

    def update(self, viz_info):
        if viz_info is None:
            return

        for body_id in viz_info.keys():
            body_viz_info = viz_info[body_id]
            body_path = self.calculate_body_path(body_viz_info)
            if body_id not in self.body_patches:
                self.body_patches[body_id] = self.draw_body(body_path, body_viz_info)
            else:
                self.body_patches[body_id].set_xy(body_path)

        self.fig.canvas.flush_events()

    def calculate_body_path(self, body_viz_info):
        x = body_viz_info["x"]
        y = body_viz_info["y"]
        angle = body_viz_info["angle"]
        body_type = body_viz_info["type"]
        raw_body_path = config.POLY_PATHS[body_type]
        rotation_matrix = np.array(
            [
                [np.cos(angle), np.sin(angle)],
                [-np.sin(angle), np.cos(angle)],
            ]
        )
        rotated_path = raw_body_path @ rotation_matrix
        body_path = rotated_path + np.array([[x, y]])
        return body_path

    def draw_body(self, body_path, body_viz_info):
        body_patch = self.ax.add_patch(
            patches.Polygon(
                body_path,
                facecolor=config.FACECOLOR[body_viz_info["type"]],
                edgecolor=config.EDGECOLOR[body_viz_info["type"]],
                linewidth=config.GAME_LINEWIDTH,
                zorder=2,
            )
        )
        return body_patch
