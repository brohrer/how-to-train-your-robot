import time
import numpy as np

n_iterations = 10000

elapsed_times = np.zeros(n_iterations)
for i_iteration in range(n_iterations):
    start_time = time.time()
    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_times[i_iteration] = elapsed_time

average_time_us = np.mean(elapsed_times) * 1e6
print(f"Average time: {average_time_us:.06} us")
for time in elapsed_times[:120]:
    print(time * 1e6)
