import json
import logging
from logging import FileHandler, Formatter
import time
from getkey import getkey

# valid levels are {DEBUG, INFO, WARNING, ERROR, CRITICAL}
logging_level = logging.INFO

log_name = f"{int(time.time())}_interface.log"
logger = logging.getLogger("interface")
logger.setLevel(logging_level)
logger_file_handler = FileHandler(log_name)
logger_file_handler.setLevel(logging_level)
logger_file_handler.setFormatter(Formatter("%(message)s"))
logger.addHandler(logger_file_handler)


def run(q):
    last_key = "0"
    while True:
        key = getkey()
        key_time = time.time()

        if key in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            q.put((key_time, key))

            log_dict = {"ts": key_time, "ppl_reported": key}
            logger.info(json.dumps(log_dict))
            last_key = key

        if key == " ":
            remove_ppl = str(-int(last_key))
            q.put((key_time, remove_ppl))

            log_dict = {"ts": key_time, "ppl_undo": last_key}
            logger.info(json.dumps(log_dict))
            last_key = "0"
