import time
from pacemaker import Pacemaker

clock_freq_hz = 4
clock_period = 1 / float(clock_freq_hz)
pacemaker = Pacemaker(clock_freq_hz)


def run(q):
    ppl_count = 0
    while True:
        overtime = pacemaker.beat()
        if overtime > clock_period:
            print(f"ts: {time.time()}, overtime: {overtime}")

        while not q.empty():
            timestamp, ppl = q.get()
            print(f"ts: {timestamp}, ppl_added: {ppl}")

            ppl_count += int(ppl)
            print(f"ts: {timestamp}, ppl_count: {ppl_count}")
