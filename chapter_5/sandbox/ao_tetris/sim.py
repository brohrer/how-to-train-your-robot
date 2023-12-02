import json
import logging_setup
import time

import config
from crystal import Crystal
from pacemaker import Pacemaker
from walls import Walls


def run(q):
    logger = logging_setup.get_logger("sim", config.LOGGING_LEVEL_SIM)
    sim = Simulation()
    pacemaker = Pacemaker(config.CLOCK_FREQ_SIM)

    # Updating the q can slow down the simulation.
    # Converting the terrain array to JSON is a slow process.
    # Only update it approximately twice per frame.
    # Once per frame might lead to lost-frame glitches, which could
    # be noticeable.
    steps_per_q_update = int(
        config.CLOCK_FREQ_SIM / (1 * config.CLOCK_FREQ_VIZ)
    )
    steps_since_q_update = 0

    i_over = 0.0
    i_total = 0.0
    while True:
        overtime = pacemaker.beat()

        i_total += 1
        if overtime > config.CLOCK_PERIOD_SIM * 0.5:
            i_over += 1
            print(
                f"sim over {int(100 * overtime / config.CLOCK_PERIOD_SIM)}%"
                + " this iteration"
                + f"  {100 * i_over / i_total:.2f}% cumulative"
            )

        if overtime > config.CLOCK_PERIOD_SIM:
            logger.error(json.dumps({"ts": time.time(), "overtime": overtime}))

        state = sim.step()
        ts = time.time()

        steps_since_q_update += 1
        if steps_since_q_update >= steps_per_q_update:
            logger.debug(json.dumps({"ts": ts, "state": state}))
            q.put((ts, state))
            steps_since_q_update = 0


class Simulation:
    def __init__(self):
        self.crystals = []
        self.walls = Walls()

        # Add a crystal containing immovable atoms.
        self.crystals.append(Crystal(config.TERRAIN))

        self.crystals.append(Crystal(config.L_CRYSTAL))

        # Add right wall
        self.walls.add_wall(
            x_left=config.FIG_WIDTH,
            y_left=1.0,
            x_right=config.FIG_WIDTH,
            y_right=0.0,
        )
        # Add left wall
        self.walls.add_wall(
            x_left=0.0,
            y_left=0.0,
            x_right=0.0,
            y_right=1.0,
        )
        # Add floor
        self.walls.add_wall(
            x_left=1.0,
            y_left=0.0,
            x_right=0.0,
            y_right=0.0,
        )
        # Add ceiling
        self.walls.add_wall(
            x_left=0.0,
            y_left=config.FIG_HEIGHT,
            x_right=1.0,
            y_right=config.FIG_HEIGHT,
        )

    def step(self):
        for crystal in self.crystals:
            crystal.start_step()

        # Calculate and tally up all the forces that act on atoms.
        for crystal in self.crystals:
            crystal.calculate_internal_forces()

        for i in range(len(self.crystals)):
            for j in range(i + 1, len(self.crystals)):
                self.crystals[i].calculate_external_forces(self.crystals[j])

        for crystal in self.crystals:
            crystal.calculate_wall_forces(self.walls)

        # Add in some gravity
        for crystal in self.crystals:
            crystal.fy += config.GRAVITY * crystal.m

        # Update atoms' positions based on the forces that act on them.
        for crystal in self.crystals:
            crystal.update_positions()

        state = self.get_state()
        return state

    def get_state(self):
        state = {}
        for crystal in self.crystals:
            state[crystal.name] = crystal.get_state()
        return state
