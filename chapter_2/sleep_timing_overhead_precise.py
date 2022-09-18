import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter


def sleep(duration):
    start = time.monotonic()
    end = start + duration
    while time.monotonic() < end:
        pass


def measure():
    max_duration = 1
    nominal = 10 ** (np.linspace(-5, -1, 4 * 10 + 1))
    measured = np.zeros(nominal.size)

    for i_nom, nom in enumerate(nominal):
        # Cap the iteration time
        n_iterations = int(
            np.maximum(1, np.minimum(1e4, max_duration / nom)))
        sleep_times = np.zeros(n_iterations)
        for i_iteration in range(n_iterations):
            start_time = time.monotonic()
            sleep(nom)
            end_time = time.monotonic()
            sleep_time = end_time - start_time
            sleep_times[i_iteration] = sleep_time

        median_time = np.median(sleep_times)
        measured[i_nom] = median_time
        print(nom, median_time)

    np.save("measured_precise.npy", measured)
    np.save("nominal_precise.npy", nominal)


def plot():
    # Convert to microseconds
    measured = np.load("measured_precise.npy") * 1e3  # ms
    nominal = np.load("nominal_precise.npy") * 1e3  # ms

    overshoot = (measured - nominal) * 1e3  # us
    log_nominal = np.log10(nominal)

    fig = plt.figure()
    ax = fig.gca()
    ax.scatter(nominal, overshoot)
    ax.grid()
    ax.set_xlabel("Nominal sleep() duration (ms)")
    ax.set_ylabel("Sleep overtime (us)")
    # ax.set_ylim(0, .6)
    plt.savefig("sleep_timing_overhead_precise_linear.png")

    fig = plt.figure()
    ax = fig.gca()
    ax.scatter(log_nominal, overshoot)
    ax.grid()
    ax.grid(which="minor", axis="x", linestyle=":", linewidth=.5)
    ax.set_xlabel("Nominal sleep() duration (ms)")
    ax.set_ylabel("Sleep overtime (us)")
    # ax.set_ylim(0, .6)

    x_major_vals = np.array([0.01, 0.1, 1, 10, 100])
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
    x_locator = FixedLocator(np.log10(x_minor_vals))
    ax.xaxis.set_minor_locator(x_locator)

    plt.savefig("sleep_timing_overhead_precise_logx.png")


measure()
plot()
