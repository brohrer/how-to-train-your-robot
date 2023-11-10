import logging
from logging import FileHandler, Formatter
import os
import time


def get_logger(name, level):
    log_name = f"{int(time.time())}_{name}.log"
    os.makedirs("logs", exist_ok=True)
    pathname = os.path.join("logs", log_name)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger_file_handler = FileHandler(pathname)
    logger_file_handler.setLevel(level)
    logger_file_handler.setFormatter(Formatter("%(message)s"))
    logger.addHandler(logger_file_handler)
    return logger
