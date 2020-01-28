#############################################################################
""" LogAllOn.py """

from LogBase import LogBase
#import logging
#import sys

##############################################################################
##############################################################################
##############################################################################
##############################################################################

class LogAllOn(LogBase):

    def __init__(self, systemLogger):
        super().__init__(systemLogger)
        return

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)
        return

    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)
        return

        ######################################################################

    def debugf(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)
        return

    def infof(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)
        return

        ######################################################################

    def debugs(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)
        return

    def infos(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)
        return

##############################################################################
##############################################################################
##############################################################################
##############################################################################
