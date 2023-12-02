import os
import time

# https://pypi.org/project/getkey/
from getkey import getkey, keys
import config


def run(keys_sim_keys_q, run_keys_alive_q):
    alive_check_interval = 1 / config.ALIVE_CHECK_FREQ
    last_alive_check = time.time()
    time_last_keypress = time.time()
    # TODO Figure out a way to send a regular heartbeat to the runner.
    # Because this process sits and waits for the user to press a key,
    # it's blocked in between keypresses. There's no way for the
    # runner to know whether it has crashed or whether it's just
    # waiting for the human to press another key.
    # alive_send_interval = 1 / config.HEARTBEAT_FREQ_KEYS
    # last_alive_send = time_time()

    while True:
        key = getkey()

        if (time.time() - last_alive_check) > alive_check_interval:
            runner_is_alive = False
            while not run_keys_alive_q.empty():
                runner_is_alive = run_keys_alive_q.get()
            if not runner_is_alive:
                os._exit(os.EX_OK)
            else:
                last_alive_check = time.time()

        if (
            time.time() - time_last_keypress
            < config.KEYPRESS_REFRACTORY_PERIOD
        ):
            continue

        if key in [
            keys.UP,
            keys.DOWN,
            keys.LEFT,
            keys.RIGHT,
            "u",
            "d",
            "l",
            "r",
            "q",
            " ",
        ]:
            # Hit q to kill the simulation
            if key == keys.UP:
                key = "u"
            if key == keys.DOWN:
                key = "d"
            if key == keys.LEFT:
                key = "l"
            if key == keys.RIGHT:
                key = "r"
            keys_sim_keys_q.put(key)

            time_last_keypress = time.time()
