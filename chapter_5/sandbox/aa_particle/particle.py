import multiprocessing as mp
import simulation as sim
import animation as ani

q = mp.Queue()
p_sim = mp.Process(target=sim.run, args=(q,))
p_ani = mp.Process(target=ani.run, args=(q,))

p_sim.start()
p_ani.start()
