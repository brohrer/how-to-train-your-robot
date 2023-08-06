import multiprocessing as mp
import dash
import sim
import viz

mp.set_start_method("fork")
timing_q = mp.Queue()
viz_q = mp.Queue()
p_dash = mp.Process(target=dash.run, args=(timing_q,))
p_sim = mp.Process(target=sim.run, args=(timing_q, viz_q))
p_viz = mp.Process(target=viz.run, args=(viz_q,))

p_dash.start()
p_sim.start()
p_viz.start()
