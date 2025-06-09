import logging
import sys

logger = logging.getLogger("Bernardson Logger")
logger.setLevel(logging.DEBUG)

# Filter out Discord logs
logging.getLogger("discord").setLevel(logging.ERROR)
logging.getLogger("discord.http").setLevel(logging.ERROR)
logging.getLogger("websockets").setLevel(logging.ERROR)

# Info handler to stdout (DEBUG and INFO only)
info_handler = logging.StreamHandler(sys.stdout)
info_handler.setLevel(logging.DEBUG)
info_handler.addFilter(lambda record: record.levelno < logging.WARNING)
info_handler.setFormatter(logging.Formatter(
    "[INFO] %(asctime)s - %(message)s", "%H:%M:%S"))

# Error handler to stderr (ERROR and CRITICAL only)
error_handler = logging.StreamHandler(sys.stderr)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    "[ERROR] %(asctime)s - %(message)s", "%H:%M:%S"))

logger.addHandler(info_handler)
logger.addHandler(error_handler)
