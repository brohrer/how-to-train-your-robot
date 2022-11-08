import numpy as np
import matplotlib.pyplot as plt


def right_triangle():
    dt = 37
    fig = plt.figure()
    ax = fig.gca()
    vals = np.cumsum(np.ones(dt))
    ax.bar(vals, vals, width=.5)
    plt.savefig("right_triangle.png", dpi=300)


def left_triangle():
    dt = 37
    fig = plt.figure()
    ax = fig.gca()
    vals = np.cumsum(np.ones(dt))
    ax.bar(vals, vals[::-1], width=.5)
    plt.savefig("left_triangle.png", dpi=300)


def isosceles_triangle():
    dt = 37
    fig = plt.figure()
    ax = fig.gca()
    right = np.cumsum(np.ones(dt))
    left = np.cumsum(np.ones(dt))[::-1]
    tri = np.minimum(right, left)
    ax.bar(right, tri, width=.5)
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
    plt.savefig("summed_triangle.png", dpi=300)


# right_triangle()
# left_triangle()
# isosceles_triangle()
summed_triangle()
