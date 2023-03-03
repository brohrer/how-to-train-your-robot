import multiprocessing as mp
import ab_simulation as sim
import ab_animation as ani

q = mp.Queue()
p_sim = mp.Process(target=sim.run, args=(q,))
p_ani = mp.Process(target=ani.run, args=(q,))

p_sim.start()
p_ani.start()
