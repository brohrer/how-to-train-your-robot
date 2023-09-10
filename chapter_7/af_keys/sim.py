import json
import tools.logging_setup as logging_setup
import os
import time
import numpy as np
from numba import njit

import config
from body import Body
from tools.pacemaker import Pacemaker
from walls import Walls


def run(
    keys_sim_keys_q,
    sim_dash_duration_q,
    sim_viz_info_q,
    run_sim_alive_q,
    sim_run_alive_q,
):
    logger = logging_setup.get_logger("sim", config.LOGGING_LEVEL_SIM)
    sim = Simulation()

    # Warm up the simulation and give everything a chance to be
    # compiled and initialized. This can take a few seconds.
    print("Warming up simulation")
    sim.warmup()

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

        keys = []
        while not keys_sim_keys_q.empty():
            keys.append(keys_sim_keys_q.get())

        # Handle keypresses
        for key in keys:
            # "q" is the code to quit the program
            if key == "q":
                print("  byeeee")
                os._exit(os.EX_OK)
            else:
                sim.command(key)

        step_duration = sim.step()

        sim_dash_duration_q.put(step_duration)

        steps_since_viz_q_update += 1
        if steps_since_viz_q_update >= steps_per_viz_q_update:
            viz_info = sim.get_viz_info()
            ts = time.time()
            logger.debug(json.dumps({"ts": ts, "viz_info": viz_info}))
            sim_viz_info_q.put((ts, viz_info))
            steps_since_viz_q_update = 0


class Simulation:
    def __init__(self):
        self.bodies = {}
        ship_params = config.SHIP_BODY
        self.ship_id = ship_params["id"]
        self.bodies[self.ship_id] = Body(ship_params)

        a0_params = config.A0_BODY
        a0_id = a0_params["type"] + "_00"
        a0_params["id"] = a0_id
        self.bodies[a0_id] = Body(a0_params)

        self.walls = Walls()
        for wall_init in config.WALLS:
            self.walls.add_wall(wall_init)

    def command(self, key):
        ship = self.bodies[self.ship_id]

        if key == "u":
            ship.f_x_ext_buffer.add(
                config.FORCE_SHAPE
                * config.FORCE_MAGNITUDE
                * np.cos(ship.angle)
            )
            ship.f_y_ext_buffer.add(
                config.FORCE_SHAPE
                * config.FORCE_MAGNITUDE
                * np.sin(ship.angle)
            )

        if key == "r":
            ship.torque_ext_buffer.add(
                config.FORCE_SHAPE * -1 * config.TORQUE_MAGNITUDE
            )

        if key == "l":
            ship.torque_ext_buffer.add(
                config.FORCE_SHAPE * config.TORQUE_MAGNITUDE
            )

    def step(self):
        # Time each pass through the computations of step().
        start = time.time()

        # Express the bodies as a list each time through.
        # This step is necessary because bodies can both come into and
        # and out of existence at any time step, but it's useful to
        # have a list of them for these next few steps.
        body_list = list(self.bodies.values())
        n_bodies = len(body_list)
        self.bodies_x = np.zeros(n_bodies)
        self.bodies_y = np.zeros(n_bodies)
        self.bodies_r = np.zeros(n_bodies)
        self.bodies_are_close = np.zeros((n_bodies, n_bodies))
        for i_body, body in enumerate(body_list):
            self.bodies_x[i_body] = body.x
            self.bodies_y[i_body] = body.y
            self.bodies_r[i_body] = body.radius

        for body in body_list:
            body.start_step()

        # Find which bodies are close enough to merit calculating interactions.
        self.calculate_proximity(body_list)

        # Calculate and tally up all the forces that act on bodies.
        for i in range(len(body_list)):
            for j in range(i + 1, len(body_list)):
                if self.bodies_are_close[i, j]:
                    body_list[i].calculate_interactions(body_list[j])

        for body in body_list:
            body.calculate_wall_forces(self.walls)

        # Add in some gravity
        if abs(config.GRAVITY) > 0:
            for body in body_list:
                body.f_y_atoms += config.GRAVITY * body.m_atoms

        # Update atoms' positions based on the forces that act on them.
        for body in body_list:
            body.update_positions()

        elapsed = time.time() - start
        return elapsed

    def warmup(self):
        """
        Numba @njit functions are compiled "just in time", that is,
        when they are first called. This function is a copy-paste
        from step() that ensures that they are each called at least once
        before the simulation kicks off in earnest. This helps
        the simulation and animation not to pause awkwardly.
        """
        body_list = list(self.bodies.values())
        n_bodies = len(body_list)
        self.bodies_x = np.zeros(n_bodies)
        self.bodies_y = np.zeros(n_bodies)
        self.bodies_r = np.zeros(n_bodies)
        self.bodies_are_close = np.zeros((n_bodies, n_bodies))
        for i_body, body in enumerate(body_list):
            self.bodies_x[i_body] = body.x
            self.bodies_y[i_body] = body.y
            self.bodies_r[i_body] = body.radius

        for body in body_list:
            body.start_step()

        self.calculate_proximity(body_list)

        # Calculate and tally up all the forces that act on bodies.
        for i in range(len(body_list)):
            for j in range(i + 1, len(body_list)):
                body_list[i].calculate_interactions(body_list[j])

        for body in body_list:
            body.calculate_wall_forces(self.walls)

        for body in body_list:
            body.update_positions()

    def calculate_proximity(self, body_list):
        for i_body, body in enumerate(body_list):
            self.bodies_x[i_body] = body.x
            self.bodies_y[i_body] = body.y

        calculate_proximity_numba(
            self.bodies_x, self.bodies_y, self.bodies_r, self.bodies_are_close
        )

    def get_viz_info(self):
        viz_info = {}
        for body in self.bodies.values():
            viz_info[body.name] = body.get_viz_info()
        return viz_info


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
