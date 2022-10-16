from pacemaker import Pacemaker
import numpy as np

clock_freq_hz = 2
pacemaker = Pacemaker(clock_freq_hz)

ppl_count = 0
while True:
    overtime = pacemaker.beat()

    ppl = np.random.randint(9)
    ppl_count += int(ppl)
    print(f"ppl_added: {ppl},  total_ppl: {ppl_count}")
