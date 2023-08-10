from time import perf_counter
import numpy as np
from numba import njit, prange

n_reps = 10
n_elements = int(1e8)


@njit
def add_numpy_jit(A, B, C):
    C = A + B
    return C


@njit
def add_elements(A, B, C):
    for i in range(A.size):
        C[i] = A[i] + B[i]
    return C


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
A = np.random.sample(n_elements)
B = np.random.sample(n_elements)
C = np.random.sample(n_elements)

# Ensure jitted functions are pre-compiled
add_numpy_jit(A, B, C)
add_elements(A, B, C)

time_function(np.add, "Numpy array addition")
time_function(add_numpy_jit, "Numpy array addition, jitted by Numba ")
time_function(add_elements, "Numba-jitted element-wise array addition")
