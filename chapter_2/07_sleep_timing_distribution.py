import time
import numpy as np
import matplotlib.pyplot as plt

n_iterations = 1000
n_bins = np.arange(10, 10.5, .01)
sleep_duration = .01

sleep_times = np.zeros(n_iterations)
for i_iteration in range(n_iterations):
    start_time = time.monotonic()
    time.sleep(sleep_duration)
    end_time = time.monotonic()
    sleep_time = end_time - start_time
    sleep_times[i_iteration] = sleep_time * 1000  # ms

average_time = np.mean(sleep_times)
print(
    "Average sleep time:",
    f"{average_time:.09} seconds")
for time in sleep_times[:12]:
    print(time)

fig = plt.figure()
ax = fig.gca()
ax.hist(sleep_times, bins=n_bins)

y_max = ax.get_ylim()[1]
tick_height = - y_max / 48
offset = - y_max / 128
for sleep_time in sleep_times:
    ax.plot(
        [sleep_time, sleep_time],
        [offset, tick_height],
        color="black",
        linewidth=.5,
        solid_capstyle="round",
    )
ax.set_xlim(10, 10.5)

ax.set_xlabel("Actual time (ms)")
ax.set_ylabel("Count")
plt.savefig("sleep_time_distribution.png", dpi=300)
plt.show()
