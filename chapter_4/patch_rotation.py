import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from pacemaker import Pacemaker

path_filename = "insignia.npy"


def main():
    pacemaker = Pacemaker(24)
    path = np.load(path_filename)
    fig, patch = initialize_animation(path)

    for i in range(1000):
        step_animation(patch, path, i)
        fig.canvas.flush_events()
        pacemaker.beat()


def initialize_animation(path):
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    patch = ax.add_patch(
        patches.Polygon(
            path,
            facecolor="seagreen",
            edgecolor="darkgreen",
            linewidth=3,
            joinstyle="miter",
        )
    )

    plt.ion()
    plt.show()

    return fig, patch


def step_animation(patch, base_path, i):

    path = np.copy(base_path)
    theta = i / 10
    # pendulum angle
    angle = 0.5 * np.sin(theta)

    dy_pre = -1
    dy_post = 1 + 20 * (1 - np.cos(angle))
    scale = 2.5

    # Rotation transformation
    rotation = np.array(
        [
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)],
        ]
    )

    path[:, 1] = path[:, 1] + dy_pre
    path = scale * path @ rotation
    path[:, 1] = path[:, 1] + dy_post

    patch.set_xy(path)


def save_path():
    points = [
        [4.94, 1.21],
        [5.55, 2.45],
        [5.92, 4.21],
        [5.13, 3.25],
        [3.86, 4.51],
        [4.25, 2.55],
    ]
    uncentered_path = np.array(points)
    center = np.array([4.94, 2.92])
    path = uncentered_path - center
    path[:, 1] = -1 * path[:, 1]

    np.save(path_filename, path)


main()
