import json
import logging_setup
import time

import config
from body import Body
from pacemaker import Pacemaker
from walls import Walls


def run(sim_dash_duration_q, sim_viz_state_q):
    logger = logging_setup.get_logger("sim", config.LOGGING_LEVEL_SIM)
    sim = Simulation()

    # Warm up the simulation and give everything a chance to be
    # initialized. This can take 10 seconds or more.
    print("Warming up simulation")
    sim.step()

    pacemaker = Pacemaker(config.CLOCK_FREQ_SIM)

    # Updating a Queue can slow down the simulation.
    # Converting the terrain array to JSON is a slow process.
    # Only update it approximately once per frame.
    steps_per_viz_q_update = int(
        config.CLOCK_FREQ_SIM / (1 * config.CLOCK_FREQ_VIZ)
    )
    steps_since_viz_q_update = 0

    # i_over = 0.0
    # i_total = 0.0
    while True:
        overtime = pacemaker.beat()

        # i_total += 1
        # if overtime > config.CLOCK_PERIOD_SIM * 0.5:
        #     i_over += 1
        #     print(
        #         f"sim over {int(100 * overtime / config.CLOCK_PERIOD_SIM)}%"
        #         + " this iteration"
        #         + f"  {100 * i_over / i_total:.2f}% cumulative"
        #     )

        if overtime > config.CLOCK_PERIOD_SIM:
            logger.warning(
                json.dumps({"ts": time.time(), "overtime": overtime})
            )

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
        for body_init in config.BODIES:
            self.bodies.append(Body(body_init))

        self.walls = Walls()
        for wall_init in config.WALLS:
            self.walls.add_wall(wall_init)

    def step(self):
        # Time each pass through the computations of step().
        start = time.time()

        for body in self.bodies:
            body.start_step()

        # Calculate and tally up all the forces that act on bodies.
        for i in range(len(self.bodies)):
            for j in range(i + 1, len(self.bodies)):
                self.bodies[i].calculate_interactions(self.bodies[j])

        for body in self.bodies:
            body.calculate_wall_forces(self.walls)

        # Add in some gravity
        if config.GRAVITY > 0:
            for body in self.bodies:
                body.f_y_atoms += config.GRAVITY * body.m_atoms

        # Update atoms' positions based on the forces that act on them.
        for body in self.bodies:
            body.update_positions()

        elapsed = time.time() - start
        return elapsed

    def get_state(self):
        state = {}
        for body in self.bodies:
            state[body.name] = body.get_state()
        return state
