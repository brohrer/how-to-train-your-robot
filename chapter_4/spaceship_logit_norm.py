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
        size = np.random.randint(3) + 0.5
        color = np.random.choice([light_blue, light_gray])
        ax.plot(x, y, marker=marker, markersize=size, color=color, zorder=0)

    plt.ion()
    plt.show()

    return fig, patch


def generate_trajectory():
    pi = np.pi
    # dx, dy, dtheta, i_start, i_end
    movements = [
        [8, 4, 0, 0, 44],
        [0, 0, - pi * 0.65, 27, 38],
        [2, -11, 0, 26, 76],
        [0, 0, - pi * .75, 57, 68],
        [-10, 7, 0, 54, 102],
        [0, 0, - pi * 0.6, 94, 102],
    ]
    trip_length = 104
    x_init = -5
    y_init = 0
    theta_init = pi * 1.7
    vy = np.zeros(trip_length)
    vx = np.zeros(trip_length)
    vtheta = np.zeros(trip_length)

    for i_move in range(len(movements) - 1):
        dx, dy, dtheta, i_start, i_end = movements[i_move]
        dt = i_end - i_start + 1

        mu = np.random.normal(0, 0.3)
        sigma = np.random.normal(0.7, 0.1)
        t = np.linspace(1e-6, 1 - 1e-6, dt)
        logit_norm = (
            1
            / (t * (1 - t))
            * np.exp(-1 * (np.log(t / (1 - t)) - mu) ** 2 / (2 * sigma**2))
        )
        logit_norm *= 1 / (np.sum(logit_norm) + 1e-6)
        vx[i_start: i_end + 1] += logit_norm * dx
        vy[i_start: i_end + 1] += logit_norm * dy
        vtheta[i_start: i_end + 1] += logit_norm * dtheta

    x = x_init + np.cumsum(vx)
    y = y_init + np.cumsum(vy)
    theta = theta_init + np.cumsum(vtheta)

    return x, y, theta


def step_animation(patch, base_path, x, y, theta, i):
    j = i % x.size
    scale = 0.4
    rotation = np.array(
        [
            [np.cos(theta[j]), np.sin(theta[j])],
            [-np.sin(theta[j]), np.cos(theta[j])],
        ]
    )
    translation = np.array([[x[j], y[j]]])
    path = scale * base_path @ rotation + translation
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
