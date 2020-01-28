##############################################################################
##############################################################################
""" Utilities.py """
from datetime import datetime
import time


class Utilities():

    @staticmethod
    def getTimeStampSecs():
        return int(round(datetime.now().timestamp()))

    @staticmethod
    def getTimeStampSecsAsStr():
        return str(Utilities.getTimeStampSecs())

    @staticmethod
    def getTimeStampMsecs():
        return time.time_ns()

    @staticmethod
    def getTimeStampMsecsAsStr():
        return str(Utilities.getTimeStampMsecs())


##############################################################################
##############################################################################
