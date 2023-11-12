import time
import numpy as np
from numba import njit


# 42 ms with Numba
# 17 ms without Numba

# 39 ms with Numba
# 17 ms without Numba
# @njit
def add(A, B, C):
    C = A + B
    return C

# Fails to compile with Numba
# 14 ms without Numba
# @njit
# def add(A, B, C):
#     np.add(A, B, out=C)
#     return C

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
