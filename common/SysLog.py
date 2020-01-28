#############################################################################
""" SysLog.py """

import logging
from logging.handlers import TimedRotatingFileHandler
import sys

##############################################################################
##############################################################################
##############################################################################
##############################################################################

_logger = None

def getLogger():
    """ docstring """
    #global _logger
    return _logger

def setLogger(slg):
    """ docstring """
    global _logger
    _logger = slg
    return _logger

##############################################################################
##############################################################################
##############################################################################
##############################################################################

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

_moduleName = __name__

_logFormatter = "%(asctime)s — %(name)s — %(levelname)s — %(message)s"

_fileName = "sysLogger.log"


def initialize(moduleName="", fileName="", logFmtr="", level=logging.DEBUG):
    """ Get the logger, set its console and file handlers
            Best to call only once
    """
    global _moduleName, _logFormatter

    if moduleName:
        _moduleName = moduleName
    if logFmtr:
        _logFormatter = logFmtr
    formatter = logging.Formatter(_logFormatter)

    _lggr = logging.getLogger(_moduleName)
    _lggr.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    _lggr.addHandler(handler)

    handler = TimedRotatingFileHandler(fileName, when='midnight', backupCount=3)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    _lggr.addHandler(handler)

    _lggr.propagate = False        # don't propagate the error up to parent

    return setLogger(_lggr)


# ##############################################################################
# ##############################################################################
# ##############################################################################
# ##############################################################################



# """

# def get_console_handler():
#     """ Return the handler for the console and set its formatter """
#     console_handler = logging.StreamHandler(sys.stdout)
#     console_handler.setFormatter(LOG_FORMATTER)
#     return console_handler

# def get_file_handler():
#     """ Get the handler for the log file and set its formatter """
#     file_handler = TimedRotatingFileHandler(LOG_FILE_NAME, when='midnight')
#     file_handler.setFormatter(LOG_FORMATTER)
#     return file_handler

# def get_logger(logger_name, level):
#     """ Get the logger, set its console and file handlers """
#     lggr = logging.getLogger(logger_name)
#     lggr.setLevel(level)
#     lggr.addHandler(get_console_handler())
#     lggr.addHandler(get_file_handler())
#     lggr.propagate = False        # don't propagate the error up to parent
#     return lggr


# #logger = get_logger(__name__, logging.CRITICAL)
# #logger = get_logger(__name__, logging.ERROR)
# #logger = get_logger(__name__, logging.WARNING)
# #logger = get_logger(__name__, logging.INFO)
# logger = get_logger(__name__, logging.DEBUG)
# #logger = get_logger(__name__, logging.NOTSET)

# logger.info("Log Started")

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

# if __name__ == '__main__':
    # initialize(moduleName="myName", fileName="", logFmtr="", level=logging.DEBUG)
    # lllevel = logging.DEBUG
    # initialize(moduleName="name", fileName="fileName.log", logFmtr="%(asctime)s — %(name)s — %(levelname)s — %(message)s", level=lllevel)
    # initialize("name", "fileName.log", "%(asctime)s — %(name)s — %(levelname)s — %(message)s", logging.DEBUG)
    # logger = getLogger()
    # logger.debug("Testing the log")
    # logger.debug("Testing the log")
    # logger.debug("Testing the log")
    # logger.debug("Testing the log")
    # logger.debug("Testing the log")
    # logger.debug("Testing the log")
    # logger.debug("Testing the log")
    # logger.debug("Testing the log")

###
#############################################################################
