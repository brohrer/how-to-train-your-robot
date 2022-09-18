import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter


def measure():
    max_duration = 100
    # nominal = 10 ** (np.linspace(-6, 1, 7 * 7 + 1))
    nominal = 10 ** (np.linspace(-5, -1, 4 * 20 + 1))
    measured = np.zeros(nominal.size)

    for i_nom, nom in enumerate(nominal):
        # Cap the iteration time
        n_iterations = int(
            np.maximum(1, np.minimum(1e4, max_duration / nom)))
        sleep_times = np.zeros(n_iterations)
        for i_iteration in range(n_iterations):
            start_time = time.monotonic()
            time.sleep(nom)
            end_time = time.monotonic()
            sleep_time = end_time - start_time
            sleep_times[i_iteration] = sleep_time

        median_time = np.median(sleep_times)
        measured[i_nom] = median_time
        print(nom, median_time)

    np.save("measured.npy", measured)
    np.save("nominal.npy", nominal)


def plot():
    # Convert to milliseconds
    measured = np.load("measured.npy") * 1000
    nominal = np.load("nominal.npy") * 1000

    overshoot = measured - nominal
    log_nominal = np.log10(nominal)

    # zoom_cap = .1
    # nominal_zoom = nominal[np.where(nominal <= zoom_cap)]
    # log_nominal_zoom = log_nominal[np.where(nominal <= zoom_cap)]
    # overshoot_zoom = overshoot[np.where(nominal <= zoom_cap)]

    fig = plt.figure()
    ax = fig.gca()
    ax.scatter(nominal, overshoot)
    ax.grid()
    ax.set_xlabel("Nominal sleep() duration (ms)")
    ax.set_ylabel("Sleep overtime (ms)")
    ax.set_ylim(0, .6)
    plt.savefig("sleep_timing_overhead_linear.png")

    fig = plt.figure()
    ax = fig.gca()
    ax.scatter(log_nominal, overshoot)
    ax.grid()
    ax.grid(which="minor", axis="x", linestyle=":", linewidth=.5)
    ax.set_xlabel("Nominal sleep() duration (ms)")
    ax.set_ylabel("Sleep overtime (ms)")
    ax.set_ylim(0, .6)

    x_major_vals = np.array([
        0.01, 0.1, 1, 10, 100])
    #     0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30, 100])
    x_formatter = FixedFormatter(x_major_vals)
    x_locator = FixedLocator(np.log10(x_major_vals))
    ax.xaxis.set_major_formatter(x_formatter)
    ax.xaxis.set_major_locator(x_locator)

    x_minor_vals = np.array([
        .01, .02, .03, .04, .05, .06, .07, .08, .09,
        .1, .2, .3, .4, .5, .6, .7, .8, .9,
        1, 2, 3, 4, 5, 6, 7, 8, 9,
        10, 20, 30, 40, 50, 60, 70, 80, 90, 1000
    ])
    # x_formatter = FixedFormatter(x_minor_vals)
    x_locator = FixedLocator(np.log10(x_minor_vals))
    # ax.xaxis.set_minor_formatter(x_formatter)
    ax.xaxis.set_minor_locator(x_locator)

    plt.savefig("sleep_timing_overhead_logx.png")

    """
    fig = plt.figure()
    ax = fig.gca()
    ax.scatter(nominal_zoom, overshoot_zoom)
    ax.grid()
    plt.savefig("sleep_timing_overhead_linear_zoom.png")

    fig = plt.figure()
    ax = fig.gca()
    ax.scatter(log_nominal_zoom, overshoot_zoom)
    ax.grid()
    plt.savefig("sleep_timing_overhead_logx_zoom.png")
    """

# measure()
plot()
