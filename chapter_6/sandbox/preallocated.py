import time
import numpy as np
from numba import njit

# pre-allocated: 68 ms
# allocated in fcn: 96 ms
# skip intermediate variable entirely: 24 ms
# no difference between square and self multiply

# do the square in the center of the for loop: 13.5 ms
# add intermediate variable: no change

# @njit
# @njit
# def add(A, B, C, D):
'''
def add(A, B, D):
    C = np.ones((n_B, n_A), dtype=float)
    for j, a in enumerate(A):
        for i, b in enumerate(B):
            C[i, j] = a - b

    D = C ** 2
    return D
'''
@njit
def add(A, B, D):
    # C = np.ones((n_B, n_A), dtype=float)
    for j, a in enumerate(A):
        for i, b in enumerate(B):
            # D[i, j] = (a - b) * (a - b)
            d = a - b
            D[i, j] = d ** 2

    # D = C ** 2
    return D


n_reps = 100
n_A = int(2e3)
n_B = int(4e3)

A = np.arange(n_A, dtype=float)
B = np.arange(n_B, dtype=float)
# C = np.ones((n_B, n_A), dtype=float)
D = np.ones((n_B, n_A), dtype=float)

D = add(A, B, D)
# D = add(A, B, C, D)

print("last", D[-1, -1])

total_time = 0
for i_rep in range(n_reps):
    A = np.arange(i_rep, n_A + i_rep, dtype=float)
    B = np.arange(i_rep, n_B + i_rep, dtype=float)

    start = time.time()

    D = add(A, B, D)
    # D = add(A, B, C, D)

    end = time.time()
    total_time += end - start

    print("last", D[-1, -1])

print("total time", total_time)
print("average time", total_time / n_reps)
