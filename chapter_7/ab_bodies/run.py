import multiprocessing as mp
import sys
import config
import dash
from pacemaker import Pacemaker
import sim
import viz

# import watch

mp.set_start_method("fork")

sim_dash_duration_q = mp.Queue()
sim_viz_state_q = mp.Queue()
# watcher_q = mp.Queue()

run_sim_alive_q = mp.Queue()
sim_run_alive_q = mp.Queue()
run_viz_alive_q = mp.Queue()
viz_run_alive_q = mp.Queue()
run_dash_alive_q = mp.Queue()
dash_run_alive_q = mp.Queue()


p_dash = mp.Process(
    target=dash.run,
    args=(
        sim_dash_duration_q,
        run_dash_alive_q,
        dash_run_alive_q,
    ),
)
p_sim = mp.Process(
    target=sim.run,
    args=(
        sim_dash_duration_q,
        sim_viz_state_q,
        run_sim_alive_q,
        sim_run_alive_q,
    ),
)
p_viz = mp.Process(
    target=viz.run,
    args=(
        sim_viz_state_q,
        run_viz_alive_q,
        viz_run_alive_q,
    ),
)

pacemaker = Pacemaker(config.CLOCK_FREQ_RUN)

# Kick off the simulation process and give it a chance to get warmed up.
p_sim.start()
sim_warmed_up = False
while not sim_warmed_up:
    pacemaker.beat()
    run_sim_alive_q.put(True)

    sim_warmed_up = False
    while not sim_run_alive_q.empty():
        sim_warmed_up = sim_run_alive_q.get()

p_dash.start()
p_viz.start()

n_alive_check = int(config.CLOCK_FREQ_RUN / config.ALIVE_CHECK_FREQ)
i_alive_check = 0
while True:
    pacemaker.beat()
    i_alive_check += 1

    # Send a health signal to the child processes.
    run_dash_alive_q.put(True)
    run_sim_alive_q.put(True)
    run_viz_alive_q.put(True)

    if i_alive_check == n_alive_check:
        all_processes_healthy = True

        dash_is_alive = False
        while not dash_run_alive_q.empty():
            dash_is_alive = dash_run_alive_q.get()
        if not dash_is_alive:
            print("Dashboard process has shut down.")
            all_processes_healthy = False

        sim_is_alive = False
        while not sim_run_alive_q.empty():
            sim_is_alive = sim_run_alive_q.get()
        if not sim_is_alive:
            print("Simulation process has shut down.")
            all_processes_healthy = False

        viz_is_alive = False
        while not viz_run_alive_q.empty():
            viz_is_alive = viz_run_alive_q.get()
        if not viz_is_alive:
            print("Visualization process has shut down.")
            all_processes_healthy = False

        if not all_processes_healthy:
            print("Shutting down all processes.")
            sys.exit()
        else:
            i_alive_check = 0
