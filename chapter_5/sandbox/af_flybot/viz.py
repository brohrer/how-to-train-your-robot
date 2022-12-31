import json
import logging_setup
import time

import numpy as np
import matplotlib.pyplot as plt

import matplotlib.patches as patches
from pacemaker import Pacemaker
from flybot_viz import BotViz
from ground_viz import GroundViz
import colors
import config
import convert_svg

FIG_HEIGHT = 6  # inches
FIG_WIDTH = 8  # inches
HORIZON_HEIGHT = 3.6  # inches
CLOUD_HEIGHT = 5.2  # inches
CLOUD_SCALE = 7
MOUNTAINS_SCALE = 20
MOUNTAINS_HEIGHT = HORIZON_HEIGHT * 0.9
BUILDINGS_SCALE = 6
BUILDINGS_HEIGHT = HORIZON_HEIGHT

SVG_FILENAME = "scene.svg"
SVG_IDS = [
    "stack",
    "stack_anchor",
    "building_0",
    "building_1",
    "building_2",
    "building_3",
    "building_4",
    "buildings_anchor",
    "mountains",
    "mountains_anchor",
    "cloud",
    "cloud_anchor",
]


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
        convert_svg.convert(SVG_FILENAME, SVG_IDS)

        self.fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
        ax = self.fig.add_axes((0, 0, 1, 1))
        ax.set_facecolor(colors.DESERT_SKY)
        ax.set_xlim(0, FIG_WIDTH)
        ax.set_ylim(0, FIG_HEIGHT)

        desert_path = np.array(
            [
                [0, HORIZON_HEIGHT],
                [0, 0],
                [FIG_WIDTH, 0],
                [FIG_WIDTH, HORIZON_HEIGHT],
            ]
        )
        ax.add_patch(
            patches.Polygon(
                desert_path,
                facecolor=colors.LIGHT_BROWN,
                edgecolor="none",
                zorder=-1,
            )
        )

        cloud_path = np.load("cloud.npy")
        cloud_anchor = np.load("cloud_anchor.npy")
        cloud_path -= np.mean(cloud_anchor, axis=0)
        cloud_path *= CLOUD_SCALE
        cloud_path += np.array([[FIG_WIDTH * 0.3, CLOUD_HEIGHT]])
        ax.add_patch(
            patches.Polygon(
                cloud_path,
                facecolor=colors.SHADOW,
                edgecolor="none",
                zorder=-3,
            )
        )

        cloud_path = np.load("cloud.npy")
        cloud_path -= np.mean(cloud_anchor, axis=0)
        cloud_path *= CLOUD_SCALE
        cloud_path += np.array([[FIG_WIDTH * 0.7, CLOUD_HEIGHT]])
        ax.add_patch(
            patches.Polygon(
                cloud_path,
                facecolor=colors.SHADOW,
                edgecolor="none",
                zorder=-3,
            )
        )

        mountains_path = np.load("mountains.npy")
        mountains_anchor = np.load("mountains_anchor.npy")
        mountains_path -= np.mean(mountains_anchor, axis=0)
        mountains_path *= MOUNTAINS_SCALE
        mountains_path += np.array([[FIG_WIDTH * 0.3, MOUNTAINS_HEIGHT]])
        ax.add_patch(
            patches.Polygon(
                mountains_path,
                facecolor=colors.BROWN,
                edgecolor="none",
                zorder=-3,
            )
        )

        mountains_path = np.load("mountains.npy")
        mountains_path -= np.mean(mountains_anchor, axis=0)
        mountains_path *= MOUNTAINS_SCALE
        mountains_path += np.array([[FIG_WIDTH * 0.7, MOUNTAINS_HEIGHT * 1.1]])
        ax.add_patch(
            patches.Polygon(
                mountains_path,
                facecolor=colors.BROWN,
                edgecolor="none",
                zorder=-3,
            )
        )

        """
        building_0_path = np.load("building_0.npy")
        buildings_anchor = np.load("buildings_anchor.npy")
        building_0_path -= np.mean(buildings_anchor, axis=0)
        building_0_path *= BUILDINGS_SCALE
        building_0_path += np.array([[FIG_WIDTH, BUILDINGS_HEIGHT]])
        ax.add_patch(
            patches.Polygon(
                building_0_path,
                facecolor=colors.BROWN,
                edgecolor=colors.SHADOW,
                linewidth=0.5,
                zorder=-3,
            )
        )

        building_1_path = np.load("building_1.npy")
        buildings_anchor = np.load("buildings_anchor.npy")
        building_1_path -= np.mean(buildings_anchor, axis=0)
        building_1_path *= BUILDINGS_SCALE
        building_1_path += np.array([[FIG_WIDTH, BUILDINGS_HEIGHT]])
        ax.add_patch(
            patches.Polygon(
                building_1_path,
                facecolor=colors.BUILDING_GRAY,
                edgecolor=colors.SHADOW,
                linewidth=0.5,
                zorder=-2,
            )
        )

        building_2_path = np.load("building_2.npy")
        buildings_anchor = np.load("buildings_anchor.npy")
        building_2_path -= np.mean(buildings_anchor, axis=0)
        building_2_path *= BUILDINGS_SCALE
        building_2_path += np.array([[FIG_WIDTH, BUILDINGS_HEIGHT]])
        ax.add_patch(
            patches.Polygon(
                building_2_path,
                facecolor=colors.BUILDING_GRAY,
                edgecolor=colors.SHADOW,
                linewidth=0.5,
                zorder=-2,
            )
        )

        building_3_path = np.load("building_3.npy")
        buildings_anchor = np.load("buildings_anchor.npy")
        building_3_path -= np.mean(buildings_anchor, axis=0)
        building_3_path *= BUILDINGS_SCALE
        building_3_path += np.array([[FIG_WIDTH, BUILDINGS_HEIGHT]])
        ax.add_patch(
            patches.Polygon(
                building_3_path,
                facecolor=colors.BUILDING_GRAY,
                edgecolor=colors.SHADOW,
                linewidth=0.5,
                zorder=-4,
            )
        )

        building_4_path = np.load("building_4.npy")
        buildings_anchor = np.load("buildings_anchor.npy")
        building_4_path -= np.mean(buildings_anchor, axis=0)
        building_4_path *= BUILDINGS_SCALE
        building_4_path += np.array([[FIG_WIDTH, BUILDINGS_HEIGHT]])
        ax.add_patch(
            patches.Polygon(
                building_4_path,
                facecolor=colors.BUILDING_GRAY,
                edgecolor=colors.SHADOW,
                linewidth=0.5,
                zorder=-4,
            )
        )
        """

        return ax

    def update(self, state):
        if state is None:
            return

        self.bot.update(state["bot"])
        self.ground.update(state["ground"])

        self.fig.canvas.flush_events()
