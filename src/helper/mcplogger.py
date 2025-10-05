""" logger setup """
import logging
import logging.config

# Configure logging
logging.config.fileConfig("logging.conf")

# Create a logger instance
logger = logging.getLogger("evmcp")
