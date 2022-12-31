import numpy as np
import matplotlib.patches as patches
import colors
import convert_svg

SVG_FILENAME = "flybot.svg"
SVG_IDS = ["body", "head", "mask", "eye", "arm", "pack"]


class BotViz:
    def __init__(self, ax):
        self.x = 0
        self.y = 0

        convert_svg.convert(SVG_FILENAME, SVG_IDS)

        self.body_path = np.load("body.npy")
        self.body_patch = ax.add_patch(
            patches.Polygon(
                self.body_path,
                facecolor=colors.BODY_EGGSHELL,
                edgecolor=colors.MASK_BLACK,
                linewidth=0.5,
                zorder=2,
            )
        )

        self.pack_path = np.load("pack.npy")
        self.pack_patch = ax.add_patch(
            patches.Polygon(
                self.pack_path,
                facecolor=colors.BODY_EGGSHELL,
                edgecolor=colors.MASK_BLACK,
                linewidth=0.5,
                zorder=2,
            )
        )

        self.head_path = np.load("head.npy")
        self.head_patch = ax.add_patch(
            patches.Polygon(
                self.head_path,
                facecolor=colors.BODY_EGGSHELL,
                edgecolor=colors.MASK_BLACK,
                linewidth=0.5,
                zorder=2,
            )
        )

        self.arm_path = np.load("arm.npy")
        self.arm_patch = ax.add_patch(
            patches.Polygon(
                self.arm_path,
                facecolor=colors.BODY_EGGSHELL,
                edgecolor=colors.MASK_BLACK,
                linewidth=0.5,
                zorder=3,
            )
        )

        self.mask_path = np.load("mask.npy")
        self.mask_patch = ax.add_patch(
            patches.Polygon(
                self.mask_path,
                facecolor=colors.MASK_BLACK,
                edgecolor="none",
                zorder=1,
            )
        )

        self.eye_path = np.load("eye.npy")
        self.eye_patch = ax.add_patch(
            patches.Polygon(
                self.eye_path,
                facecolor=colors.EYE_BLUE,
                edgecolor="none",
                zorder=2,
            )
        )

    def update(self, state):
        self.x = state["x"]
        self.y = state["y"]
        offset = np.array([[self.x, self.y]])

        self.head_patch.set_xy(self.head_path + offset)
        self.body_patch.set_xy(self.body_path + offset)
        self.pack_patch.set_xy(self.pack_path + offset)
        self.arm_patch.set_xy(self.arm_path + offset)
        self.mask_patch.set_xy(self.mask_path + offset)
        self.eye_patch.set_xy(self.eye_path + offset)

        # print(np.max(self.body_path, axis=0), np.min(self.body_path, axis=0))
