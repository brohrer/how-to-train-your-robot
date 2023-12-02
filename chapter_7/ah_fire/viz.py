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

        self.skin_classes = {
            "ship": ShipSkin,
            "torpedo": TorpedoSkin,
            "a0": AsteroidSkin,
        }
        self.skins = {}

    def update(self, viz_info):
        if viz_info is None:
            return

        for body_id in viz_info.keys():
            body_update_info = viz_info[body_id]

            if body_id not in self.skins:
                SkinClass = self.skin_classes[body_update_info["type"]]
                self.skins[body_id] = SkinClass(body_update_info, self.ax)
            else:
                self.skins[body_id].update(body_update_info)

        skins_to_remove = []
        for skin_id in self.skins.keys():
            if skin_id not in viz_info:
                skins_to_remove.append(skin_id)

        for skin in skins_to_remove:
            try:
                self.skins[skin_id].remove()
            except KeyError:
                # Already removed
                pass
            try:
                del self.skins[skin_id]
            except KeyError:
                # Already removed
                pass

        self.fig.canvas.flush_events()


class Skin:
    """
    Skins are expected to have these methods at a minimum.
    """

    def __init__(self):
        pass

    def update(self, params):
        pass

    def remove(self, params):
        pass


class ShipSkin:
    def __init__(self, state, ax):
        self.ax = ax
        self.path = config.POLY_PATHS["ship"]
        self.facecolor = config.FACECOLOR["ship"]
        self.edgecolor = config.EDGECOLOR["ship"]
        self.linewidth = config.LINEWIDTH["ship"]

        path = transform_path(
            self.path, x=state["x"], y=state["y"], angle=state["angle"]
        )

        self.patch = self.ax.add_patch(
            patches.Polygon(
                path,
                facecolor=self.facecolor,
                edgecolor=self.edgecolor,
                linewidth=self.linewidth,
                zorder=2,
            )
        )

    def update(self, state):
        path = transform_path(
            self.path, x=state["x"], y=state["y"], angle=state["angle"]
        )
        self.patch.set_xy(path)

    def remove(self):
        self.patch.remove()


class TorpedoSkin:
    def __init__(self, state, ax):
        self.ax = ax
        self.path = config.POLY_PATHS["torpedo"]
        self.facecolor = config.FACECOLOR["torpedo"]
        self.edgecolor = config.EDGECOLOR["torpedo"]
        self.linewidth = config.LINEWIDTH["torpedo"]

        path = transform_path(
            self.path, x=state["x"], y=state["y"], angle=state["angle"]
        )

        self.patch = self.ax.add_patch(
            patches.Polygon(
                path,
                facecolor=self.facecolor,
                edgecolor=self.edgecolor,
                linewidth=self.linewidth,
                zorder=2,
            )
        )

    def update(self, state):
        path = transform_path(
            self.path, x=state["x"], y=state["y"], angle=state["angle"]
        )
        self.patch.set_xy(path)

    def remove(self):
        self.patch.remove()


class AsteroidSkin:
    def __init__(self, state, ax):
        self.ax = ax
        asteroid_type = state["type"]
        self.path = config.POLY_PATHS[asteroid_type]
        self.facecolor = config.FACECOLOR[asteroid_type]
        self.edgecolor = config.EDGECOLOR[asteroid_type]
        self.linewidth = config.LINEWIDTH[asteroid_type]

        path = transform_path(
            self.path, x=state["x"], y=state["y"], angle=state["angle"]
        )

        self.patch = self.ax.add_patch(
            patches.Polygon(
                path,
                facecolor=self.facecolor,
                edgecolor=self.edgecolor,
                linewidth=self.linewidth,
                zorder=2,
            )
        )

    def update(self, state):
        path = transform_path(
            self.path, x=state["x"], y=state["y"], angle=state["angle"]
        )
        self.patch.set_xy(path)

    def remove(self):
        self.patch.remove()


def transform_path(base_path, x=0, y=0, angle=0, scale=1):
    rotation_matrix = np.array(
        [
            [np.cos(angle), np.sin(angle)],
            [-np.sin(angle), np.cos(angle)],
        ]
    )

    scaled_path = base_path * scale
    rotated_path = scaled_path @ rotation_matrix
    body_path = rotated_path + np.array([[x, y]])
    return body_path
