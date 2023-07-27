import time
import numpy as np

n_reps = 100
n_sum = int(1e7)  # 18 ms

total_time = 0
for i_rep in range(n_reps):
    A = np.arange(i_rep, n_sum + i_rep)
    B = np.arange(i_rep, n_sum + i_rep)

    start = time.time()

    C = A + B

    end = time.time()
    total_time += end - start

    print("last", C[-1])

print("total time", total_time)
print("average time", total_time / n_reps)
