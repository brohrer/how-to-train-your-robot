import time
import numpy as np

n_iterations = 10000

total_execution_time = 0
for _ in range(n_iterations):
    start_time = time.time()

    # Do some time consuming busywork computation
    size_3D = (100, 100, 100)
    random_array = np.random.sample(size=size_3D)
    total = np.sum(random_array)

    end_time = time.time()
    elapsed_time = end_time - start_time
    total_execution_time += elapsed_time

average_time = total_execution_time / n_iterations
print(
    "Average execution time:",
    f"{average_time:.09} seconds")
