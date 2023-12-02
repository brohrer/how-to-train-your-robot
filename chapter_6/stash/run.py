import multiprocessing as mp
import sys
import time
import config
import dash
from pacemaker import Pacemaker
import sim
import viz
import watch

mp.set_start_method("fork")

timing_q = mp.Queue()
viz_q = mp.Queue()
watcher_q = mp.Queue()

p_dash = mp.Process(target=dash.run, args=(timing_q,))
p_sim = mp.Process(target=sim.run, args=(timing_q, viz_q))
p_viz = mp.Process(target=viz.run, args=(viz_q,))

p_dash.start()
p_sim.start()
p_viz.start()

time.sleep(config.WARMUP_PERIOD)

p_watch = mp.Process(target=watch.run, args=(
    watcher_q, [p_dash, p_sim, p_viz]))
p_watch.start()

pacemaker = Pacemaker(config.CLOCK_FREQ_RUN)
while True:
    pacemaker.beat()

    # Send a health signal to the watcher process.
    watcher_q.put(True)

    healthy = True
    if not p_dash.is_alive():
        print("Dashboard process has shut down.")
        healthy = False
    if not p_sim.is_alive():
        print("Simulation process has shut down.")
        healthy = False
    if not p_viz.is_alive():
        print("Visualization process has shut down.")
        healthy = False
    if not p_watch.is_alive():
        print("Runner monitoring process has shut down.")
        healthy = False

    if not healthy:
        print("Shutting down all processes.")
        '''
        try:
            p_dash.kill()
        except Exception:
            pass

        try:
            p_sim.kill()
        except Exception:
            pass

        try:
            p_viz.kill()
        except Exception:
            pass

        try:
            p_watch.kill()
        except Exception:
            pass
        '''
        sys.exit()
