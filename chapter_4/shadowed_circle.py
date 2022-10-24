import numpy as np
import matplotlib.pyplot as plt
from pacemaker import Pacemaker


def main():
    pacemaker = Pacemaker(24)
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    circles = draw_circles(ax)
    plt.ion()
    plt.show()

    for i in range(1000):
        move_circles(circles, i)
        fig.canvas.flush_events()
        pacemaker.beat()


def draw_circles(ax):
    """
    Create a sequence of a main ball,
    together with three trailing shadows.
    Each shadow is a little lighter
    in color than the one before,
    and each one occludes--is drawn
    on top of--the one behind it.
    """
    ball = ax.plot(
        0,
        0,
        color="#4682b4",
        marker="o",
        markersize=24,
        zorder=3,
    )[0]
    shadow_1 = ax.plot(
        0,
        0,
        color="#a7c4dd",
        marker="o",
        markersize=24,
        zorder=2,
    )[0]
    shadow_2 = ax.plot(
        0,
        0,
        color="#d3e2ee",
        marker="o",
        markersize=24,
        zorder=1,
    )[0]
    shadow_3 = ax.plot(
        0,
        0,
        color="#e9f0f6",
        marker="o",
        markersize=24,
        zorder=0,
    )[0]
    return (ball, shadow_1, shadow_2, shadow_3)


def move_circles(circles, i):
    """
    Advance the ball and each of its shadows
    along a Lissajous curve.
    The shadows have a lag compared to
    main ball, introduced by subtracting
    a few iterations from i.
    """
    (ball, shadow_1, shadow_2, shadow_3) = circles

    ball.set_xdata(np.sin(i / 16))
    ball.set_ydata(np.sin(i / 14))

    shadow_1.set_xdata(np.sin((i - 1) / 16))
    shadow_1.set_ydata(np.sin((i - 1) / 14))

    shadow_2.set_xdata(np.sin((i - 3) / 16))
    shadow_2.set_ydata(np.sin((i - 3) / 14))

    shadow_3.set_xdata(np.sin((i - 6) / 16))
    shadow_3.set_ydata(np.sin((i - 6) / 14))


main()
