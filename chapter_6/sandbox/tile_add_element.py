import time
import numpy as np
from numba import njit

# No njit: 1357 ms
# njit: 24 ms
# @njit
def add(A, B, C):
    for j, a in enumerate(A):
        for i, b in enumerate(B):
            C[i, j] = a - b
    return C


n_reps = 100
n_A = int(2e3)
n_B = int(4e3)

A = np.arange(n_A, dtype=float)
B = np.arange(n_B, dtype=float)
C = np.ones((n_B, n_A), dtype=float)

C = add(A, B, C)

print("last", C[-1, -1])

total_time = 0
for i_rep in range(n_reps):
    A = np.arange(i_rep, n_A + i_rep, dtype=float)
    B = np.arange(i_rep, n_B + i_rep, dtype=float)

    start = time.time()

    C = add(A, B, C)

    end = time.time()
    total_time += end - start

    print("last", C[-1, -1])

print("total time", total_time)
print("average time", total_time / n_reps)
