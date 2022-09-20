import time
import numpy as np
import matplotlib.pyplot as plt

count_from_first_iteration = True
clock_freq_Hz = 20
collection_duration = 120
n_iterations = int(clock_freq_Hz * collection_duration)
n_bins = np.arange(-.5, .5, .01)

clock_period = 1 / float(clock_freq_Hz)
t0 = time.monotonic()
this_run_completed = time.time()
last_completed = t0

errors = np.zeros(n_iterations)
for i_iter in range(n_iterations):

    if count_from_first_iteration:
        # end time tied to start of first iteration
        end = t0 + (i_iter + 1) * clock_period
    else:
        # end time tied to start of current iteration
        end = last_completed + clock_period

    wait = end - time.monotonic()
    if wait > 0:
        time.sleep(wait)

    completed = time.monotonic()
    duration = completed - last_completed
    error = duration - clock_period
    errors[i_iter] = error * 1000  # ms
    last_completed = completed

print(f"Average error {np.mean(errors)} ms")
print(f"Median error {np.median(errors)} ms")

fig = plt.figure()
ax = fig.gca()
ax.hist(errors, bins=n_bins)

y_max = ax.get_ylim()[1]
tick_height = - y_max / 48
offset = - y_max / 128
for error in errors:
    ax.plot(
        [error, error],
        [offset, tick_height],
        color="black",
        linewidth=.5,
        solid_capstyle="round",
    )

ax.set_xlabel("Error (ms)")
ax.set_ylabel("Count")
plt.savefig("metronome_errors.png", dpi=300)
plt.show()
