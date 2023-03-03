import logging
from logging import FileHandler, Formatter
import time


def get_logger(name, level):
    log_name = f"{int(time.time())}_{name}.log"
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger_file_handler = FileHandler(log_name)
    logger_file_handler.setLevel(level)
    logger_file_handler.setFormatter(Formatter("%(message)s"))
    logger.addHandler(logger_file_handler)
    return logger
