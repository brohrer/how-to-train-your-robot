from time import perf_counter
import numpy as np
from numba import njit, prange


@njit
def matmul(A, B, C):
    n_row, n_col = C.shape
    n_mid = A.shape[1]
    for i in range(n_row):
        for j in range(n_col):
            for k in range(n_mid):
                C[i, j] += A[i, k] * B[k, j]


@njit(parallel=True)
def matmul_parallel(A, B, C):
    n_row, n_col = C.shape
    n_mid = A.shape[1]
    for i in prange(n_row):
        for j in prange(n_col):
            for k in prange(n_mid):
                C[i, j] += A[i, k] * B[k, j]


n_reps = 20

n_rows = 1000
n_mid = 1000
n_cols = 1000

# Initialize and pre-allocate the arrays
A = np.random.sample((n_rows, n_mid))
B = np.random.sample((n_mid, n_cols))
C = np.random.sample((n_rows, n_cols))

# Ensure jitted functions are pre-compiled
matmul(A, B, C)
matmul_parallel(A, B, C)

#
# Time Numpy matrix multiplication
print()
print("Numpy matrix multiply")
total_time = 0
for i_rep in range(n_reps):
    print(f"iter {i_rep + 1} of {n_reps}", end="\r")

    start = perf_counter()
    C = A @ B
    end = perf_counter()
    total_time += end - start

print(f"average time per call: {int(1000 * total_time / n_reps)} ms")

#
# Time single-process Numba-optimized, naively implemented
# matrix multiplication
print()
print("Numba, single-process matrix multiply")
total_time = 0
for i_rep in range(n_reps):
    print(f"iter {i_rep + 1} of {n_reps}", end="\r")

    start = perf_counter()
    matmul(A, B, C)
    end = perf_counter()
    total_time += end - start

print(f"average time per call: {int(1000 * total_time / n_reps)} ms")

#
# Time parallelized Numba-optimized matrix multiplication
print()
print("Numba, parallelized matrix multiply")
total_time = 0
for i_rep in range(n_reps):
    print(f"iter {i_rep + 1} of {n_reps}", end="\r")

    start = perf_counter()
    matmul_parallel(A, B, C)
    end = perf_counter()
    total_time += end - start

print(f"average time per call: {int(1000 * total_time / n_reps)} ms")
