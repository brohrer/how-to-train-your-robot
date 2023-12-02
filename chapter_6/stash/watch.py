import sys
from pacemaker import Pacemaker
import config


def run(run_watch_heartbeat_q, processes):

    pacemaker = Pacemaker(config.CLOCK_FREQ_WATCH)

    while True:
        pacemaker.beat()
        is_alive = False

        while not run_watch_heartbeat_q.empty():
            _ = run_watch_heartbeat_q.get()
            is_alive = True

        if not is_alive:
            print("Runner process has shut down.")
            print("Shutting down all processes.")
            for process in processes:
                try:
                    process.kill()
                except Exception:
                    pass

            sys.exit()
