import numpy as np
import matplotlib.pyplot as plt


def right_triangle():
    dt = 37
    fig = plt.figure()
    ax = fig.gca()
    vals = np.cumsum(np.ones(dt))
    ax.bar(vals, vals, width=.5)
    ax.set_xlabel("frame number")
    ax.set_ylabel("speed")
    plt.savefig("right_triangle.png", dpi=300)


def left_triangle():
    dt = 37
    fig = plt.figure()
    ax = fig.gca()
    vals = np.cumsum(np.ones(dt))
    ax.bar(vals, vals[::-1], width=.5)
    ax.set_xlabel("frame number")
    ax.set_ylabel("speed")
    plt.savefig("left_triangle.png", dpi=300)


def isosceles_triangle():
    dt = 37
    fig = plt.figure()
    ax = fig.gca()
    right = np.cumsum(np.ones(dt))
    left = np.cumsum(np.ones(dt))[::-1]
    tri = np.minimum(right, left)
    ax.bar(right, tri, width=.5)
    ax.set_xlabel("frame number")
    ax.set_ylabel("speed")
    plt.savefig("isosceles_triangle.png", dpi=300)


def summed_triangle():
    dt = 37
    fig = plt.figure()
    ax = fig.gca()
    right = np.cumsum(np.ones(dt))
    left = np.cumsum(np.ones(dt))[::-1]
    tri = np.minimum(right, left)
    tri = tri / np.sum(tri)
    tri_pos = np.cumsum(tri)
    ax.bar(right, tri_pos, width=.5)
    ax.set_xlabel("frame number")
    ax.set_ylabel("normalized progress")
    plt.savefig("summed_triangle.png", dpi=300)


def min_jerk():
    t = np.linspace(0, 1, 100)
    x = 10 * t ** 3 - 15 * t ** 4 + 6 * t ** 5
    v = np.diff(x) * (t.size - 1)

    fig = plt.figure()
    ax = fig.gca()
    ax.plot(t, x)
    ax.set_xlabel("normalized time")
    ax.set_ylabel("normalized progress")
    ax.grid()
    plt.savefig("min_jerk_progress.png", dpi=300)

    fig = plt.figure()
    ax = fig.gca()
    ax.plot(t[1:], v)
    ax.set_xlabel("normalized time")
    ax.set_ylabel("normalized speed")
    ax.grid()
    plt.savefig("min_jerk_speed.png", dpi=300)


def logit_normal():
    t = np.linspace(.001, .999, 100)
    mu = 0
    sigma = .7
    v = (
        1 / (t * (1 - t)) * np.exp(
        -1 * (np.log(t / (1 - t)) - mu) ** 2 /
        (2 * sigma ** 2)))
    x = np.cumsum(v)

    fig = plt.figure()
    ax = fig.gca()
    ax.plot(t, x)
    ax.set_xlabel("normalized time")
    ax.set_ylabel("normalized progress")
    ax.grid()
    plt.savefig("logit_norm_progress.png", dpi=300)

    fig = plt.figure()
    ax = fig.gca()
    ax.plot(t, v)
    ax.set_xlabel("normalized time")
    ax.set_ylabel("normalized speed")
    ax.grid()
    plt.savefig("logit_norm_speed.png", dpi=300)


right_triangle()
left_triangle()
isosceles_triangle()
summed_triangle()
min_jerk()
logit_normal()
