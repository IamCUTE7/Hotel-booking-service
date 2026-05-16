import os
import sys

from loguru import logger


def setup_logging():
    level = os.getenv("LOG_LEVEL", "INFO")

    logger.remove()

    fmt = "<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>"
    logger.add(sys.stdout, level=level, format=fmt)

    return logger
