import time
import numpy as np
from numba import njit

@njit
def add(A, B, C):
    I, J = np.shape(A)
    for i in range(I):
            C[i, 0] = A[i, 0] + B[i, 0]
    return C


n_reps = 100
n_rows = int(1e7)

A = np.arange(n_rows)
B = np.arange(n_rows)
C = np.arange(n_rows)

C = C[:, np.newaxis]

C = add(A[:, np.newaxis], B[:, np.newaxis], C)

print("last", C[-1])

total_time = 0
for i_rep in range(n_reps):
    A = np.arange(i_rep, n_rows + i_rep)
    B = np.arange(i_rep, n_rows + i_rep)

    start = time.time()

    C = add(A[:, np.newaxis], B[:, np.newaxis], C)

    end = time.time()
    total_time += end - start

    print("last", C[-1])

print("total time", total_time)
print("average time", total_time / n_reps)

