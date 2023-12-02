
import time
import numpy as np
from numba import njit

# No njit: 47 ms
# njit: 139 ms
# @njit
def add(A, B, C, row_tile, col_tile):
    C = (row_tile @ A) - (B @ col_tile)
    return C


n_reps = 100
n_A = int(2e3)
n_B = int(4e3)

A = np.arange(n_A, dtype=float)[np.newaxis, :]
B = np.arange(n_B, dtype=float)[:, np.newaxis]
C = np.ones((n_B, n_A))

row_tile = np.ones((n_B, 1), dtype=float)
col_tile = np.ones((1, n_A), dtype=float)

C = add(A, B, C, row_tile, col_tile)

print("last", C[-1, -1])

total_time = 0
for i_rep in range(n_reps):
    A = np.arange(i_rep, n_A + i_rep, dtype=float)[np.newaxis, :]
    B = np.arange(i_rep, n_B + i_rep, dtype=float)[:, np.newaxis]

    start = time.time()

    C = add(A, B, C, row_tile, col_tile)

    end = time.time()
    total_time += end - start

    print("last", C[-1, -1])

print("total time", total_time)
print("average time", total_time / n_reps)
