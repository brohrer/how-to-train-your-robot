import json
import logging
from logging import FileHandler, Formatter
import time
from pacemaker import Pacemaker

# valid levels are {DEBUG, INFO, WARNING, ERROR, CRITICAL}
logging_level = logging.INFO

log_name = f"{int(time.time())}_adder.log"
logger = logging.getLogger("adder")
logger.setLevel(logging_level)
logger_file_handler = FileHandler(log_name)
logger_file_handler.setLevel(logging_level)
logger_file_handler.setFormatter(Formatter("%(message)s"))
logger.addHandler(logger_file_handler)

clock_freq_hz = 4
clock_period = 1 / float(clock_freq_hz)
pacemaker = Pacemaker(clock_freq_hz)


def run(q):
    ppl_count = 0
    while True:
        overtime = pacemaker.beat()
        if overtime > clock_period:
            log_dict = {"ts": time.time(), "overtime": overtime}
            logger.error(json.dumps(log_dict))

        while not q.empty():
            timestamp, ppl = q.get()

            log_dict = {"ts": timestamp, "ppl_added": ppl}
            logger.debug(json.dumps(log_dict))

            ppl_count += int(ppl)

            log_dict = {"ts": timestamp, "ppl_count": ppl_count}
            logger.info(json.dumps(log_dict))

            print(f"    {ppl_count} people ", end="\r")
