import multiprocessing as mp
import aa_simulation as sim
import aa_animation as ani

q = mp.Queue()
p_sim = mp.Process(target=sim.run, args=(q,))
p_ani = mp.Process(target=ani.run, args=(q,))

p_sim.start()
p_ani.start()
