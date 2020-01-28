####################################################################
""" TopicMaker.py """
#import sys
#import logging
#import json
#from ActiveNIF import ActiveNIF
import Constants
#from ConfigReaderWriter import ConfigReaderWriter
#import SysLog
#from Utilities import Utilities

###################################################################
###################################################################
###################################################################
###################################################################

_SEP = "/"
_WILDCARD = "#"

_REQ    = "Req"
_RSP    = "Rsp"
_DHCP   = "Dhcp"
_SIGNON = "Signon"
_CMD    = "Cmd"
_ERRORS = "Errors"
_MISC   = "Misc"
_ALL    = "All"

_TOPIC_DHCP_ALL_REQ = _DHCP + _ALL + _REQ
_TOPIC_DHCP_ALL_RSP = _DHCP + _ALL + _RSP
_TOPIC_DHCP_REQ     = _DHCP + _REQ
_TOPIC_DHCP_RSP     = _DHCP + _RSP


class TopicMaker():

    #_macAddr

    def __init__(self, macAddr):
        self._macAddr = macAddr

    @staticmethod
    def makeTopicDhcpAllReq():
        return _TOPIC_DHCP_ALL_REQ

    @staticmethod
    def makeTopicDhcpAllRsp():
        return _TOPIC_DHCP_ALL_RSP

    @staticmethod
    def makeTopicDhcpReq():
        return _TOPIC_DHCP_REQ

    def makeTopicDhcpRsp(self):
        return self._macAddr + _SEP + _TOPIC_DHCP_RSP

    def makeTopicSignonReq(self):
        """
            cmd = mac/SignonReq or root/mac/SignonReq
            Published by
        """
        return self._macAddr + _SEP + _SIGNON + _REQ

    def makeTopicSignonRsp(self):
        """
            cmd = mac/SignonRsp or root/mac/SignonRsp
            Subscribed to
        """
        return self._macAddr + _SEP + _SIGNON + _RSP

    #staticmethod
    def makeTopicSubscribeAll():
        return Constants.CFG_MQTT_SUBSCRIBE_ALL

    def makeTopicCmdReq(self):
        return self._macAddr + _SEP + _CMD + _REQ

    def makeTopicCmdRsp(self):
        return self._macAddr + _SEP + _CMD + _RSP

    def makeTopicMisc(self):
        return self._macAddr + _SEP + _MISC


###################################################################
###################################################################
###################################################################
###################################################################
