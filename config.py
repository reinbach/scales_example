import logging

DEBUG = True

LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(LOG_LEVEL)

