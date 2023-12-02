import json
import logging_setup
import os
import time
import numpy as np
from numba import njit

import config
from body import Body
from pacemaker import Pacemaker
from walls import Walls


def run(
    sim_dash_duration_q,
    sim_viz_state_q,
    run_sim_alive_q,
    sim_run_alive_q,
):
    logger = logging_setup.get_logger("sim", config.LOGGING_LEVEL_SIM)
    sim = Simulation()

    # Warm up the simulation and give everything a chance to be
    # initialized. This can take 10 seconds or more.
    print("Warming up simulation")
    sim.step()

    pacemaker = Pacemaker(config.CLOCK_FREQ_SIM)
    n_alive_check = int(config.CLOCK_FREQ_SIM / config.ALIVE_CHECK_FREQ)
    i_alive_check = 0

    # Updating a Queue can slow down the simulation.
    # Converting the terrain array to JSON is a slow process.
    # Only update it approximately once per frame.
    steps_per_viz_q_update = int(
        config.CLOCK_FREQ_SIM / (1 * config.CLOCK_FREQ_VIZ)
    )
    steps_since_viz_q_update = 0

    while True:
        overtime = pacemaker.beat()
        if overtime > config.CLOCK_PERIOD_SIM:
            logger.warning(
                json.dumps({"ts": time.time(), "overtime": overtime})
            )

        # Send a heartbeat from this process to the parent runner process,
        # reassuring it that everything here is okie dokie.
        sim_run_alive_q.put(True)

        # Watch for a heartbeat from the parent runner process.
        # If it is not found, then shut down this process too.
        i_alive_check += 1

        if i_alive_check == n_alive_check:
            runner_is_alive = False
            while not run_sim_alive_q.empty():
                runner_is_alive = run_sim_alive_q.get()
            if not runner_is_alive:
                print("Runner process has shut down.")
                print("Shutting down simulation process.")
                # sys.exit()
                os._exit(os.EX_OK)
            else:
                i_alive_check = 0

        step_duration = sim.step()

        sim_dash_duration_q.put(step_duration)

        steps_since_viz_q_update += 1
        if steps_since_viz_q_update >= steps_per_viz_q_update:
            state = sim.get_state()
            ts = time.time()
            logger.debug(json.dumps({"ts": ts, "state": state}))
            sim_viz_state_q.put((ts, state))
            steps_since_viz_q_update = 0


class Simulation:
    def __init__(self):
        self.bodies = []
        for body_id, body_init in config.BODIES.items():
            self.bodies.append(Body(body_init))
        n_bodies = len(self.bodies)
        self.bodies_x = np.zeros(n_bodies)
        self.bodies_y = np.zeros(n_bodies)
        self.bodies_r = np.zeros(n_bodies)
        self.bodies_are_close = np.zeros((n_bodies, n_bodies))
        for i_body, body in enumerate(self.bodies):
            self.bodies_x[i_body] = body.x
            self.bodies_y[i_body] = body.y
            self.bodies_r[i_body] = body.radius

        self.walls = Walls()
        for wall_init in config.WALLS:
            self.walls.add_wall(wall_init)

    def step(self):
        # Time each pass through the computations of step().
        start = time.time()

        for body in self.bodies:
            body.start_step()

        # Find which bodies are close enough to merit calculating interactions.
        self.calculate_proximity()

        # Calculate and tally up all the forces that act on bodies.
        for i in range(len(self.bodies)):
            for j in range(i + 1, len(self.bodies)):
                if self.bodies_are_close[i, j]:
                    self.bodies[i].calculate_interactions(self.bodies[j])

        for body in self.bodies:
            body.calculate_wall_forces(self.walls)

        # Add in some gravity
        if abs(config.GRAVITY) > 0:
            for body in self.bodies:
                body.f_y_atoms += config.GRAVITY * body.m_atoms

        # Update atoms' positions based on the forces that act on them.
        for body in self.bodies:
            body.update_positions()

        elapsed = time.time() - start
        return elapsed

    def calculate_proximity(self):
        for i_body, body in enumerate(self.bodies):
            self.bodies_x[i_body] = body.x
            self.bodies_y[i_body] = body.y

        calculate_proximity_numba(
            self.bodies_x, self.bodies_y, self.bodies_r, self.bodies_are_close
        )

    def get_state(self):
        state = {}
        for body in self.bodies:
            state[body.name] = body.get_state()
        return state


@njit
def calculate_proximity_numba(x, y, r, is_close):
    n = x.size
    for i_row in range(n):
        for j_col in range(i_row + 1, n):
            is_close[i_row, j_col] = 0
            d_x = x[i_row] - x[j_col]
            d_y = y[i_row] - y[j_col]
            distance = (d_x**2 + d_y**2) ** 0.5
            compression = r[i_row] + r[j_col] - distance
            if compression > 0:
                is_close[i_row, j_col] = 1
