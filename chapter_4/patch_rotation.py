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


def step_animation(patch, path, i):
    """
    Handle scaling, rotation, and translation of the patch at each time step.
    """
    # Step 1: Anchoring
    # Move the path so that the anchor sits at (0, 0)
    anchor = np.array([[0, 1]])
    anchored_path = path - anchor

    # Step 2: Scaling
    scale = 2.5
    scaled_path = anchored_path * scale

    # Step 3: Rotation
    # `theta` tracks the progress through the cyclical motion.
    # Every time `theta` reaches a multiple of 2 * pi
    # the cycle will start over.
    theta = i / 10
    # `angle` is the actual pendulum angle, measured as a deviation from
    # the original position.
    angle = 0.5 * np.sin(theta)
    # The rotation transformation matrix
    rotation = np.array(
        [
            [np.cos(angle), np.sin(angle)],
            [-np.sin(angle), np.cos(angle)],
        ]
    )
    rotated_path = scaled_path @ rotation

    # Step 4: Translation
    x_translation = 0
    # Re-use `angle` here to get a cyclical up-and-down translation
    # that is in sync with the rotation.
    y_translation = 20 * (1 - np.cos(angle))
    translation = np.array([[x_translation, y_translation]])
    translated_path = rotated_path + translation

    # Step 5: De-anchoring
    # Undo step 1, so the original position is restored.
    transformed_path = translated_path + anchor

    patch.set_xy(transformed_path)


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
