from time import perf_counter
import numpy as np
from numba import njit, prange

n_reps = 10
n_rows = 1000
n_mid = 1000
n_cols = 1000


@njit
def matmul_elements(A, B, C):
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


def time_function(fcn, msg):
    print()
    print(msg)
    total_time = 0
    for i_rep in range(n_reps):
        print(f"iter {i_rep + 1} of {n_reps}", end="\r")

        start = perf_counter()
        fcn(A, B, C)
        end = perf_counter()
        total_time += end - start

    print(f"{int(1000 * total_time / n_reps)} ms           ")


# Initialize and pre-allocate the arrays
A = np.random.sample((n_rows, n_mid))
B = np.random.sample((n_mid, n_cols))
C = np.random.sample((n_rows, n_cols))

# Ensure jitted functions are pre-compiled
matmul_elements(A, B, C)
matmul_parallel(A, B, C)

time_function(np.matmul, "Numpy matrix multiply")
time_function(matmul_elements, "Numba, single-threaded matrix multiply")
time_function(matmul_parallel, "Numba, parallelized matrix multiply")
