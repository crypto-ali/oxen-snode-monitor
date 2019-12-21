# status_logger

import os
import logging
#from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Variables
LOG_LEVEL = os.getenv('LOG_LEVEL')
#p = Path()
#p.resolve()
#status_file = p.resolve()  / 'logs' / 'status.log'

logger = logging.getLogger(__name__)
logger_level = logging.getLevelName(LOG_LEVEL)
logger.setLevel(logger_level)


# Handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('status.log')
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%a %b %d %Y - %I:%M:%S %p')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

if __name__ == "__main__":
  logger.info("This is an INFO log.")
  logger.warning("This is a WARNING log.")