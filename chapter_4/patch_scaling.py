import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from pacemaker import Pacemaker

path_filename = "insignia.npy"


def main():
    pacemaker = Pacemaker(24)
    path = np.load(path_filename)
    fig, patch = draw_patch(path)

    for i in range(1000):
        pulse_patch(patch, path, i)
        fig.canvas.flush_events()
        pacemaker.beat()


def draw_patch(path):
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    patch = ax.add_patch(
        patches.Polygon(path, facecolor="firebrick", edgecolor="black", linewidth=2)
    )

    plt.ion()
    plt.show()

    return fig, patch


def pulse_patch(patch, path, i):
    theta = i / 7
    scale = 3 + 0.6 * (np.sin(theta) + 0.4 * np.sin(3 * theta))
    patch.set_xy(path * scale)


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
