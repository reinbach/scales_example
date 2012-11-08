import logging

DEBUG = True

LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

logging.basicConfig()

def log_init(name):
  log = logging.getLogger(name)
  log.setLevel(LOG_LEVEL)
  return log
