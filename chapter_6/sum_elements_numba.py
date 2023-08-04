import time
import numpy as np
from numba import njit


#  2300 ms without Numba
#  14 ms with Numba
@njit
def add(A, B, C):
    for i in range(n_sum):
        C[i] = A[i] + B[i]
    return C


n_reps = 100
n_sum = int(1e7)  # 1300 ms

A = np.arange(n_sum)
B = np.arange(n_sum)
C = np.arange(n_sum)


C = add(A, B, C)

print("last", C[-1])

total_time = 0
for i_rep in range(n_reps):
    A = np.arange(i_rep, n_sum + i_rep)
    B = np.arange(i_rep, n_sum + i_rep)

    start = time.time()

    C = add(A, B, C)

    end = time.time()
    total_time += end - start

    print("last", C[-1])

print("total time", total_time)
print("average time", total_time / n_reps)
