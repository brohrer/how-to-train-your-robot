import os
import time
import numpy as np
import matplotlib.pyplot as plt

n_iterations = int(1e4)
n_bins = 100
array_size = 100
figs_dirname = "figs"
os.makedirs(figs_dirname, exist_ok=True)
fig_filename = os.path.join(figs_dirname, "code_timing_distribution.png")
fig_zoom_filename = os.path.join(figs_dirname, "code_timing_distribution_zoom.png")


elapsed_times = np.zeros(n_iterations)

for i_iteration in range(n_iterations):
    start_time = time.time()

    """Do some time consuming busywork computation"""
    size_3D = (array_size, array_size, array_size)
    random_array = np.random.sample(size=size_3D)
    total = np.sum(random_array)

    end_time = time.time()

    elapsed_time = end_time - start_time
    elapsed_times[i_iteration] = elapsed_time

print(
    "Average execution time:",
    f"{np.mean(elapsed_times):.09} seconds")

fig = plt.figure()
ax = fig.gca()
ax.hist(elapsed_times, bins=n_bins)

y_max = ax.get_ylim()[1]
tick_height = - y_max / 48
offset = - y_max / 128
for elapsed_time in elapsed_times:
    ax.plot(
        [elapsed_time, elapsed_time],
        [offset, tick_height],
        color="black",
        linewidth=.5,
        solid_capstyle="round",
    )

ax.set_xlabel("Elapsed time (seconds)")
ax.set_ylabel("Count")
plt.savefig(fig_filename, dpi=300)
plt.show()

i_zoom = np.where(elapsed_times < .007)[0]
elapsed_times_zoom = elapsed_times[i_zoom]

fig_zoom = plt.figure()
ax_zoom = fig_zoom.gca()
ax_zoom.hist(elapsed_times_zoom, bins=n_bins)

y_max = ax.get_ylim()[1]
for elapsed_time in elapsed_times_zoom:
    ax_zoom.plot(
        [elapsed_time, elapsed_time],
        [offset, tick_height],
        color="black",
        linewidth=.5,
        solid_capstyle="round",
    )

ax_zoom.set_xlabel("Elapsed time (seconds)")
ax_zoom.set_ylabel("Count")

plt.savefig(fig_zoom_filename, dpi=300)
plt.show()
