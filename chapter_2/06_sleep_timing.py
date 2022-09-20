import time
import numpy as np

n_iterations = 1000
sleep_duration = .01

sleep_times = np.zeros(n_iterations)
for i_iteration in range(n_iterations):
    start_time = time.monotonic()
    time.sleep(sleep_duration)
    end_time = time.monotonic()
    sleep_time = end_time - start_time
    sleep_times[i_iteration] = sleep_time

average_time = np.mean(sleep_times)
print(
    "Average sleep time:",
    f"{average_time:.09} seconds")
