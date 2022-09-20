import time

clock_freq_Hz = 4
clock_period = 1 / float(clock_freq_Hz)

test_duration = 10  # seconds
n_iterations = int(clock_freq_Hz * test_duration)

t0 = time.monotonic()
last_completed = t0

for i_iter in range(n_iterations):

    elapsed = time.monotonic() - t0
    seconds = int(elapsed)
    milliseconds = int(elapsed * 1000) % 1000
    print(f"    {seconds}:{milliseconds:03}")

    end = t0 + (i_iter + 1) * clock_period
    wait = end - time.monotonic()
    if wait > 0:
        time.sleep(wait)
    else:
        print("We're running behind!")

    completed = time.monotonic()
    duration = completed - last_completed
    last_completed = completed
