import time

clock_freq_Hz = 2
clock_period = 1 / float(clock_freq_Hz)

test_duration = 10  # seconds
n_iterations = int(clock_freq_Hz * test_duration)

t0 = time.monotonic()
last_completed = t0

for i_iter in range(n_iterations):
    end = t0 + (i_iter + 1) * clock_period
    wait = end - time.monotonic()
    if wait > 0:
        time.sleep(wait)

    completed = time.monotonic()
    duration = completed - last_completed
    print(duration * 1000)
    last_completed = completed
