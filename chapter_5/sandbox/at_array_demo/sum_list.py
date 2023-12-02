import time

n_reps = 100
n_sum = int(1e7)  # 1300 ms

total_time = 0
for i_rep in range(n_reps):
    A = list(range(i_rep, n_sum + i_rep))
    B = list(range(i_rep, n_sum + i_rep))
    C = list(range(i_rep, n_sum + i_rep))

    start = time.time()

    for i in range(n_sum):
        C[i] = A[i] + B[i]

    end = time.time()
    total_time += end - start

    print("last", C[n_sum - 1])

print("total time", total_time)
print("average time", total_time / n_reps)
