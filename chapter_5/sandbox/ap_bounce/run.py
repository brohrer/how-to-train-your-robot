import multiprocessing as mp
import sim
import viz

mp.set_start_method("fork")
q = mp.Queue()
p_sim = mp.Process(target=sim.run, args=(q,))
p_viz = mp.Process(target=viz.run, args=(q,))

p_sim.start()
p_viz.start()
