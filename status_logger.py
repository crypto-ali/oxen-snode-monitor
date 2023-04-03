import os
import logging.handlers
from dotenv import load_dotenv

load_dotenv()

# Variables
LOG_LEVEL = os.getenv('LOG_LEVEL')
RUNNING = os.getenv('RUNNING')
LOG_SIZE = int(os.getenv('LOG_SIZE'))
LOG_BACKUPS = int(os.getenv('LOG_BACKUPS'))

logger = logging.getLogger(__name__)
logger_level = logging.getLevelName(LOG_LEVEL)
logger.setLevel(logger_level)

# Console handler
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)

# Create formatter and add it to handler
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)

# Add handler to the logger
logger.addHandler(c_handler)

if RUNNING == 'SCREEN':
    # Initialize logging file handler and file formatter
    # RotateFileHandler: status.log, append, LOG_SIZE, LOG_BACKUPS.
    f_handler = logging.handlers.RotatingFileHandler("status.log", "a", LOG_SIZE, LOG_BACKUPS)
    f_handler.setLevel(logging.DEBUG)
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                 datefmt='%a %b %d %Y - %I:%M:%S %p')
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)

if __name__ == "__main__":
    logger.debug("This is an DEBUG log.")
    logger.info("This is an INFO log.")
    logger.warning("This is a WARNING log.")
    logger.error("This is an ERROR log.")
