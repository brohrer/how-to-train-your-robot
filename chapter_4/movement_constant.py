import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from pacemaker import Pacemaker

path_filename = "insignia.npy"


def main():
    pacemaker = Pacemaker(24)
    path = np.load(path_filename)
    fig, patch = initialize_animation(path)
    x, y, theta = generate_trajectory()

    for i in range(1000):
        step_animation(patch, path, x, y, theta, i)
        fig.canvas.flush_events()
        pacemaker.beat()


def initialize_animation(path):
    """
    Palette is Westerlund 2 from
    https://starlust.org/space-color-palette/
    """
    black = "#20191a"
    rust = "#ac4139"
    light_blue = "#8ca1d2"
    light_gray = "#c2a6ae"
    brown = "#7f5153"

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_facecolor(black)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    patch = ax.add_patch(
        patches.Polygon(
            path,
            facecolor=light_gray,
            edgecolor=light_blue,
            linewidth=2,
            zorder=2,
            joinstyle="miter",
        )
    )

    # Add some stars
    n_stars = 128
    markers = ["o", ".", "x", "+", "s"]
    for _ in range(n_stars):
        x = np.random.sample() * 20 - 10
        y = np.random.sample() * 20 - 10
        marker = np.random.choice(markers)
        size = np.random.randint(3) + .5
        color = np.random.choice([light_blue, light_gray])
        ax.plot(
            x, y,
            marker=marker,
            markersize=size,
            color=color,
            zorder=0)

    plt.ion()
    plt.show()

    return fig, patch


def generate_trajectory():
    pi = np.pi
    key_sequence = [
        [-5, 0, pi * .3, 0],
        [3, 4, pi * .3, 48],
        [3, 4, pi * .95, 32],
        [5, -7, pi * .95, 54],
        [5, -7, pi * 1.7, 32],
        [-5, 0, pi * 1.7, 39],
        [-5, 0, pi * 2.3, 32],
        [-5, 0, pi * .3, 1],
    ]
    x = [key_sequence[0][0]]
    y = [key_sequence[0][1]]

    theta = [key_sequence[0][2]]
    for i_key in range(len(key_sequence) - 1):
        key_point = key_sequence[i_key]
        next_point = key_sequence[i_key + 1]
        dt = next_point[3]

        # Constant velocity
        # x += list(np.linspace(key_point[0], next_point[0], dt))
        # y += list(np.linspace(key_point[1], next_point[1], dt))
        # theta += list(np.linspace(key_point[2], next_point[2], dt))

        # Triangle velocity
        dx = next_point[0] - key_point[0]
        dy = next_point[1] - key_point[1]
        dtheta = next_point[2] - key_point[2]
        tri = np.minimum(np.cumsum(np.ones(dt)), np.cumsum(np.ones(dt))[::-1])
        tri *= 1 / np.sum(tri)
        x += list(x[-1] + np.cumsum(tri * dx))
        y += list(y[-1] + np.cumsum(tri * dy))
        theta += list(theta[-1] + np.cumsum(tri * dtheta))

        # Smooth (minimum-jerk) velocity
        dx = next_point[0] - key_point[0]
        dy = next_point[1] - key_point[1]
        dtheta = next_point[2] - key_point[2]
        tri = np.minimum(np.cumsum(np.ones(dt)), np.cumsum(np.ones(dt))[::-1])
        tri *= 1 / np.sum(tri)
        x += list(x[-1] + np.cumsum(tri * dx))
        y += list(y[-1] + np.cumsum(tri * dy))
        theta += list(theta[-1] + np.cumsum(tri * dtheta))

    x = np.array(x)
    y = np.array(y)
    theta = np.array(theta)

    return x, y, theta


def step_animation(patch, base_path, x, y, theta, i):

    j = i % x.size
    path = np.copy(base_path)
    scale = .4

    rotation = np.array(
        [
            [np.cos(theta[j]), -np.sin(theta[j])],
            [np.sin(theta[j]), np.cos(theta[j])],
        ]
    )

    translation = np.array([[x[j], y[j]]])

    path = scale * path @ rotation + translation

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
