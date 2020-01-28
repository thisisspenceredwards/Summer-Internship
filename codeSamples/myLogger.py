
##############################################################################
##############################################################################
##############################################################################
##############################################################################
"""
Add these imports for logging:
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
"""

"""
 NOTE:
   If loading logging config from a file, or using config.dictConfig, set
   disable_existing_loggers to False, otherwise, the logging will be disabled
   by default.

       logging.config.fileConfig('logging.ini', disable_existing_loggers=False)

   For dictConfig

       logging.config.dictConfig({
               'version': 1,
               'disable_existing_loggers': False,
               ....

"""


LOG_FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE_NAME = "sFlask.log"

def get_console_handler():
    """ Return the handler for the console and set its formatter """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(LOG_FORMATTER)
    return console_handler

def get_file_handler():
    """ Get the handler for the log file and set its formatter """
    file_handler = TimedRotatingFileHandler(LOG_FILE_NAME, when='midnight')
    file_handler.setFormatter(LOG_FORMATTER)
    return file_handler

def get_logger(logger_name, level):
    """ Get the logger, set its console and file handlers """
    lggr = logging.getLogger(logger_name)
    lggr.setLevel(level)
    lggr.addHandler(get_console_handler())
    lggr.addHandler(get_file_handler())
    lggr.propagate = False        # don't propagate the error up to parent
    return lggr


#logger = get_logger(__name__, logging.CRITICAL)
#logger = get_logger(__name__, logging.ERROR)
#logger = get_logger(__name__, logging.WARNING)
#logger = get_logger(__name__, logging.INFO)
logger = get_logger(__name__, logging.DEBUG)
#logger = get_logger(__name__, logging.NOTSET)

logger.info("Log Started")

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

