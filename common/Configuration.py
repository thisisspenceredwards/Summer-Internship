###################################################################
""" Configuration.py """
#import sys
#import logging
import json
import Constants
from ConfigReaderWriter import ConfigReaderWriter
import SysLog
from Utilities import Utilities

###################################################################
###################################################################
###################################################################
###################################################################

class ConfigDict:

    """ Instance Data and Methods """

    #_cfgDct = {}

    def __init__(self, cfgDct = None):
        if cfgDct is None:
            self._cfgDct = Constants.CFG_DEFAULT_DHCP_RECORD
        else:
            self._cfgDct = cfgDct
        self.setMsgFirst()
        self.setMsgLast()

    @staticmethod
    def fromJsonStr(jsonStr):
        dct = json.loads(jsonStr)
        return ConfigDict(dct)

    def getDict(self):
        return self._cfgDct

    def setDict(self, dct):
        self._cfgDct = dct


    def getGps(self):
        return self._cfgDct.get(Constants.CFG_KEY_GPS, Constants.CFG_VALUE_DEFAULT_GPS)

    def getGpsCoor(self):
        coor = (self._cfgDct[Constants.CFG_KEY_LAT], self._cfgDct[Constants.CFG_KEY_LNG])
        logger = SysLog.getLogger()
        logger.debugf('ConfigDict:getGpsCoor:lat %s lng %s' % coor)
        return coor


    def getPortBroker(self):
        return self._cfgDct.get(Constants.CFG_KEY_PORT_BROKER, Constants.CFG_VALUE_DEFAULT_PORT_BROKER)

    def getPortHttp(self):
        return self._cfgDct.get(Constants.CFG_KEY_PORT_HTTP, Constants.CFG_VALUE_DEFAULT_PORT_HTTP)


    def getIpAddr(self):
        return self._cfgDct.get(Constants.CFG_KEY_IP_ADDR, Constants.CFG_VALUE_DEFAULT_IP)

    def setIpAddr(self, ipAddr):
        self._cfgDct[Constants.CFG_KEY_IP_ADDR] = ipAddr


    def getMacAddrMaster(self):
        return self._cfgDct.get(Constants.CFG_KEY_MAC_MASTER, Constants.CFG_VALUE_DEFAULT_HEX)

    def isMacAddrMaster(self, macAddr):
        return self._cfgDct.get(Constants.CFG_KEY_MAC_MASTER, None) == macAddr


    def getMacAddrSelf(self):
        return self._cfgDct.get(Constants.CFG_KEY_MAC_SELF, Constants.CFG_VALUE_DEFAULT_HEX)


    def getMqPub(self):
        return self._cfgDct.get(Constants.CFG_KEY_MQ_PUB, Constants.CFG_VALUE_DEFAULT_STRING)

    def setMqPub(self, mqPubTopic):
        self._cfgDct[Constants.CFG_KEY_MQ_PUB] = mqPubTopic


    def getMqSub(self):
        return self._cfgDct.get(Constants.CFG_KEY_MQ_SUB, Constants.CFG_VALUE_DEFAULT_STRING)

    def setMqSub(self, mqSubTopic):
        self._cfgDct[Constants.CFG_KEY_MQ_SUB] = mqSubTopic


    def getMsgFirst(self):
        return self._cfgDct.get(Constants.CFG_KEY_MSG_FIRST, Constants.CFG_VALUE_DEFAULT_INT)

    def setMsgFirst(self):
        self._cfgDct[Constants.CFG_KEY_MSG_FIRST] = str(Utilities.getTimeStampSecs())


    def getMsgLast(self):
        return self._cfgDct.get(Constants.CFG_KEY_MSG_LAST, Constants.CFG_VALUE_DEFAULT_INT)

    def setMsgLast(self):
        self._cfgDct[Constants.CFG_KEY_MSG_LAST] = str(Utilities.getTimeStampSecs())

    def getSysName(self):
        return self._cfgDct.get(Constants.CFG_KEY_SYS_NAME, Constants.CFG_VALUE_DEFAULT_STRING)

    def getSysStatus(self):
        return self._cfgDct.get(Constants.CFG_KEY_SYS_STATUS, Constants.CFG_VALUE_DEFAULT_STRING)

    def getSysType(self):
        return self._cfgDct.get(Constants.CFG_KEY_SYS_TYPE, Constants.CFG_VALUE_DEFAULT_STRING)

    def isSlave(self):
        return self._cfgDct.get(Constants.CFG_KEY_SYS_TYPE, None) == Constants.CFG_VALUE_SYS_TYPE_SLAVE

    def getTitle(self):
        return self._cfgDct.get(Constants.CFG_KEY_TITLE, Constants.CFG_VALUE_DEFAULT_STRING)

    def setTitle(self, title):
        self._cfgDct[Constants.CFG_KEY_TITLE] = title

    def getTopicRoot(self):
        return self._cfgDct.get(Constants.CFG_KEY_TOPIC_ROOT, Constants.CFG_VALUE_DEFAULT_STRING)

    def setComment(self, comment):
        self._cfgDct[Constants.CFG_KEY_COMMENT] = comment
        return

    def getTrackTimeSecs(self):
        return self._cfgDct.get(Constants.CFG_KEY_TRACK_TIME_SECS, Constants.CFG_VALUE_DEFAULT_INT)

    def getTrackAngleEast(self):
        return self._cfgDct.get(Constants.CFG_KEY_TRACK_ANGLE_EAST, Constants.CFG_VALUE_DEFAULT_INT)

    def getTrackAngleWest(self):
        return self._cfgDct.get(Constants.CFG_KEY_TRACK_ANGLE_WEST, Constants.CFG_VALUE_DEFAULT_INT)

    def toJsonStr(self):
        return json.dumps(self.getDict(), indent=4, separators=(',', ':'))

    def updateDct(self, pHostName, pActiveNIF, sysType, comment ):
        dct = self.getDict()

        dct[Constants.CFG_KEY_PORT_HTTP] = Constants.CFG_VALUE_DEFAULT_PORT_HTTP

        dct[Constants.CFG_KEY_MSG_LAST] = str(Utilities.getTimeStampSecs())

        dct[Constants.CFG_KEY_MAC_SELF] = pActiveNIF.getMacAddrAsHexStr()
        dct[Constants.CFG_KEY_IP_ADDR] = pActiveNIF.getIpAddr()

        dct[Constants.CFG_KEY_SYS_NAME] = pHostName.get()
        dct[Constants.CFG_KEY_SYS_TYPE] = sysType

        dct[Constants.CFG_KEY_COMMENT] = comment

        return

    def updateDctFrom(self, newSlaveCfgDct ):
        dct = self.getDict()

        dct[Constants.CFG_KEY_COMMENT] = "Updated record from slave"

        dct[Constants.CFG_KEY_IP_ADDR] = newSlaveCfgDct.getIpAddr()

        dct[Constants.CFG_KEY_MSG_LAST] = Utilities.getTimeStampSecsAsStr()

        dct[Constants.CFG_KEY_SYS_STATUS] = newSlaveCfgDct.getSysStatus()

        dct[Constants.CFG_KEY_SYS_NAME] = newSlaveCfgDct.getSysName()

        return
    
    def getTotalDegreesToMove(self):
        dct = self.getDict()
        totDegs = dct[Constants.CFG_KEY_TRACK_ANGLE_WEST] - dct[Constants.CFG_KEY_TRACK_ANGLE_EAST]
        return totDegs

    def getTotalTimeToMove(self):
        dct = self.getDict()
        totSecs = dct[Constants.CFG_KEY_TRACK_TIME_SECS]
        return totSecs

    def getSecsPerDeg(self):
        totSecs = self.getTotalTimeToMove()
        totDegs = self.getTotalDegreesToMove()
        secsPerDeg = totSecs / totDegs   # how long to move rack to move 1 degree
        return 8.5  #roughly, from observation
    
    def getLatitude(self):
        dct = self.getDict()
        return dct[Constants.CFG_KEY_LATITUDE]

    def getLongitude(self):
        dct = self.getDict()
        return dct[Constants.CFG_KEY_LONGITUDE]
    
    def getSleep(self):
        dct = self.getDict()
        return dct[Constants.CFG_KEY_SLEEP]

    def getIncrementAngle(self):
        dct = self.getDict()
        return dct[Constants.CFG_KEY_INCREMENT_ANGLE]
    
    def getAzimuthAngleStart(self):
        dct = self.getDict()
        return dct[Constants.CFG_KEY_AZIMUTH_ANGLE_START]

    def getAzimuthAngleStop(self):
        dct = self.getDict()
        return dct[Constants.CFG_KEY_AZIMUTH_ANGLE_STOP]

    """ Class Data and Methods """
    #def updateWithValuesFromRemote(self, remoteDhcpDict):
    #    remoteDict = remoteDhcpDict.getDict()
    #    self._cfgDct[CFG_KEY_IP_ADDR_SELF] = remoteDict[CFG_KEY_IP_ADDR_SELF]


    def test(self):
        print(Constants.CFG_KEY_GPS,            '::', self.getGps())
        print(Constants.CFG_KEY_IP_ADDR,        '::', self.getIpAddr())
        print(Constants.CFG_KEY_MAC_MASTER,     '::', self.getMacAddrMaster())
        print(Constants.CFG_KEY_MAC_SELF,       '::', self.getMacAddrSelf())
        print(Constants.CFG_KEY_MSG_FIRST,      '::', self.getMsgFirst())
        print(Constants.CFG_KEY_MSG_LAST,       '::', self.getMsgLast())
        print(Constants.CFG_KEY_SYS_NAME,       '::', self.getSysName())
        print(Constants.CFG_KEY_SYS_TYPE,       '::', self.getSysType())
        print(Constants.CFG_KEY_TOPIC_ROOT,     '::', self.getTopicRoot())
        print(Constants.CFG_KEY_TITLE,          '::', self.getTitle())



###############################################################################
##
###############################################################################

class ConfigListOfDict:
    # a singleton: allow only one instance
    # _listOfDicts contai

    _instance = None

    def __init__(self, lofd = None):
        if not ConfigListOfDict._instance:
            ConfigListOfDict._instance = self
            if lofd is None:
                lofd = []
            self._listOfDicts = lofd

    @staticmethod
    def getInstance():
        if ConfigListOfDict._instance is None:
            ConfigListOfDict._instance = ConfigListOfDict()
        return ConfigListOfDict._instance

    def _getList(self):
        return self._listOfDicts

    def setList(self, lofd):
        self._listOfDicts = lofd

    def appendConfigDict(self, cfgdct):
        self._listOfDicts.append(cfgdct)

    @classmethod
    def readConfigFile(cls, pth, fname):
        rw = ConfigReaderWriter()
        rw.setFilePath(pth)
        rw.setFileName(fname)
        lofd = rw.read()
        return cls.fromListOfDictionaries(lofd)

    @classmethod
    def fromJsonStr(cls, jsonStr):
        lofd = json.loads(jsonStr)
        return cls.fromListOfDictionaries(lofd)

    @classmethod
    def fromListOfDictionaries(cls, lofd):
        cfgDct = []
        for dct in lofd:
            cfgDct.append(ConfigDict(dct))
        cls.getInstance().setList(cfgDct)
        return cls.getInstance()

    def toListOfDictionaries(self):
        lofd = []
        for cfgdct in self._listOfDicts:
            lofd.append(cfgdct.getDict())
        return lofd


    def debugDumpConfigLofD(self):
        print('[')
        for dct in self._listOfDicts:
            print('readConfigFile ddclofd dct=%s' % dct.getDict())
        print(']')


    def writeConfigFile(self, path, fname):
        rw = ConfigReaderWriter()
        rw.setFilePath(path)
        rw.setFileName(fname)
        lofd = self.toListOfDictionaries()
        rw.write(lofd)
        return

    def findConfigDict(self, macAddrSelf, sysType):     # 1 :: mac addr & sysType == a unique record
        for cfgdct in self._listOfDicts:
            dct = cfgdct.getDict()
            if dct[Constants.CFG_KEY_MAC_SELF] == macAddrSelf and dct[Constants.CFG_KEY_SYS_TYPE] == sysType:
                return cfgdct
        return None


    def findBrokerConfigDict(self):     # only 1
        """ return the dictionary entry for the broker system """
        for cfgdct in self._listOfDicts:
            dct = cfgdct.getDict()
            if dct[Constants.CFG_KEY_SYS_TYPE] == Constants.CFG_VALUE_SYS_TYPE_BROKER:
                return cfgdct
        return None


    def findDhcpConfigDict(self):       # only 1
        """ return the dictionary entry for the dhcp system """
        for cfgdct in self._listOfDicts:
            dct = cfgdct.getDict()
            if dct[Constants.CFG_KEY_SYS_TYPE] == Constants.CFG_VALUE_SYS_TYPE_DHCP:
                return cfgdct
        return None


    def findMasterConfigDict(self, macAddr):    # only 1
        return self.findConfigDict(macAddr, Constants.CFG_VALUE_SYS_TYPE_MASTER)
        #
        # logger = SysLog.getLogger()
        # for cfgdct in self._listOfDicts:
        #     dct = cfgdct.getDict()
        #     if dct[Constants.CFG_KEY_SYS_TYPE] == Constants.CFG_VALUE_SYS_TYPE_MASTER:
        #         thisAddr = dct[Constants.CFG_KEY_MAC_SELF]
        #         logger.debugf("this {} vs match {}".format(thisAddr, macAddr))
        #         if thisAddr == macAddr:
        #             return cfgdct
        # return None


    def findMonitorConfigDict(self, macAddr):    # only 1
        return self.findConfigDict(macAddr, Constants.CFG_VALUE_SYS_TYPE_MONITOR)


    # def findEntryForMacAddrSelf(self, selfMacAddr):
    #     for cfgDct in self._listOfDicts:
    #         dct = cfgDct.getDict()
    #             if dct[Constants.CFG_KEY_MAC_SELF] == selfMacAddr:
    #             return cfgDct
    #     return None


    # def findEntriesForSelfMacAddr(self, selfMacAddr):
    #     for dct in self._listOfDicts:
    #         if dct[Constants.CFG_KEY_MAC_SELF] == selfMacAddr:
    #             return dct
    #     return None


    # def findAllEntriesForMacAddr(self, macAddr):
    #     out = []
    #     for dct in self._listOfDicts:
    #         if dct[Constants.CFG_KEY_MAC] == macAddr:
    #             out.append(dct)
    #     return out


    def findAllSlavesForMaster(self, macMaster):    # 0 or more
        logger = SysLog.getLogger()
        logger.debugf("findAllSlavesForMaster %s BEGIN" % macMaster)
        logger.debugf("# Entries in DHCP Table: %d" % len(self._listOfDicts))
        slaves = []
        for cfgDct in self._listOfDicts:
            logger.debugf("%s %s" % (cfgDct.getSysType(), cfgDct.getMacAddrMaster()))
            if cfgDct.isSlave():
                logger.debugf("Found Slave")
                if cfgDct.isMacAddrMaster(macMaster):
                    logger.debugf("Found Master")
                    slaves.append(cfgDct)
        logger.debugf("findAllSlavesForMaster END # slaves = %d" % len(slaves))
        return slaves


    def getPortBroker(self, macAddrSelf, sysType):
        cfgDct = self.findConfigDict(macAddrSelf, sysType)
        return cfgDct.getPortBroker()

    def getGps(self, macAddrSelf, sysType):
        cfgDct = self.findConfigDict(macAddrSelf, sysType)
        return cfgDct.getGps()

    def getGpsCoor(self, macAddrSelf, sysType):
        cfgDct = self.findConfigDict(macAddrSelf, sysType)
        return cfgDct.getGpsCoor()

    def getPortHttp(self, macAddr, sysType):
        cfg = self.findConfigDict(macAddr, sysType)
        return cfg.getPortHttp()

    def getIpAddrBroker(self):
        broker = self.findBrokerConfigDict()
        return broker.getIpAddr()

    def QQQgetMacAddrMasterQQQ(self, macAddr):
        masterCfg = self.findConfigDict(macAddr, Constants.CFG_VALUE_SYS_TYPE_MASTER)
        return masterCfg.getMacAddrSelf()

    def getMacAddrOfMasterForSlave(self, slaveMacAddr):
        slaveCfg = self.findConfigDict(slaveMacAddr, Constants.CFG_VALUE_SYS_TYPE_SLAVE)
        return slaveCfg.getMacAddrMaster()

    def getTitle(self, macAddrSelf, sysType):
        cfgDct = self.findConfigDict(macAddrSelf, sysType)
        return cfgDct.getTitle()

    def toJsonStr(self):
        lofd = self.toListOfDictionaries()
        return json.dumps(lofd, indent=4, separators=(',', ':'))

    def updateCfgDct(self, rmtDct):
        lclDct = self.findConfigDict(rmtDct.getMacAddrSelf(), rmtDct.getSysType())
        if lclDct is None:                  #fle::todo::debug::why don't we have a record for this rPi?
            return None
        lclDct.updateDctFrom(rmtDct)
        return lclDct


    def updateMyCfgDict(self, hostName, activeNIF, sysType):

        logger = SysLog.getLogger()

        myMacAddr = activeNIF.getMacAddrAsHexStr()
        logger.debugf("ConfigListOfDict.updateMyCfgDict:: macAddr %s sysType %s" % (myMacAddr, sysType))

        mCfgDct = self.findConfigDict(myMacAddr, sysType)

        if mCfgDct is None:
            logger.debugf("initMyCfgDict::cfgDct not found; creating temp")
            cfgDct = ConfigDict()
            cfgDct.updateDct(hostName, activeNIF, sysType, "{} {} Temp Entry; INCOMPLETE".format(sysType, myMacAddr))
            self.appendConfigDict(cfgDct)
        else:
            logger.debugf("initMyCfgDict::Updating existing master")
            mCfgDct.updateDct(hostName, activeNIF, sysType, "{} {} Updated Entry".format(sysType, myMacAddr))

        logger.debugf("%s" % self.toJsonStr())

        return


    def updateMonitorDict(self, hostName, activeNIF):

        logger = SysLog.getLogger()
        sysType = Constants.CFG_VALUE_SYS_TYPE_MONITOR
        myMacAddr = activeNIF.getMacAddrAsHexStr()
        logger.debugf("UpdateMonitorDict BEGIN::macAddr %s sysType %s" % (myMacAddr, sysType))

        mCfgDct = self.findConfigDict(myMacAddr, sysType)
        if not mCfgDct:
            mCfgDct = self.findConfigDict("", sysType)

        if mCfgDct:
            logger.debugf("initMyCfgDict::Updating existing monitor")
            mCfgDct.updateDct(hostName, activeNIF, sysType, "{} {} Updated Entry".format(sysType, myMacAddr))
        else:
            logger.debugf("Monitor not found; creating new")
            cfgDct = ConfigDict()
            cfgDct.updateDct(hostName, activeNIF, sysType, "{} {} Temp Entry; INCOMPLETE".format(sysType, myMacAddr))
            self.appendConfigDict(cfgDct)

        logger.debugf("Monitor = %s" % self.toJsonStr())
        logger.debugf("updateMonitorDict::END")
        return


    #def updateCfgDctFrom(self, jsonStr):
    #    rmtDct = ConfigDict.fromJsonStr(jsonStr)
    #    lclDct = self.updateCfgDct(rmtDct)
    #    return lclDct

"""
following are the original routines

def _updateDct(tbdct, activeNIF, cmmt ):
    global dhcpConfigLofD

    tbdct[Constants.CFG_KEY_MSG_FIRST] = str(utilGetTimeStampSecs())
    tbdct[Constants.CFG_KEY_MSG_LAST] = str(utilGetTimeStampSecs())

    tbdct[Constants.CFG_KEY_MAC_SELF] = activeNIF.getMacAddrAsHexStr()
    tbdct[Constants.CFG_KEY_IP_ADDR_SELF] = activeNIF.getMacAddrAsHexStr()

    tbdct[Constants.CFG_KEY_SYS_NAME] = hostName.get()
    tbdct[Constants.CFG_KEY_SYS_TYPE] = Constants.CFG_VALUE_SYS_TYPE_MASTER

    tbdct[Constants.CFG_KEY_IP_ADDR_BROKER] = dhcpConfigLofD.getIpAddrBroker()

    tbdct[Constants.CFG_KEY_COMMENT] = cmmt

    return tbdct

def initMyCfgDict(dhcpCfgLofD, activeNIF):

    logger.debugf("initMyCfgDict:: {}".format(activeNIF.getMacAddrAsHexStr()))

    master = dhcpCfgLofD.findMasterConfigDict(activeNIF.getMacAddrAsHexStr())

    if master is None:
        logger.debugf("initMyCfgDict::master not found; creating temp master")
        dct = _updateDct({}, hostName, activeNIF, "Master: Initial Table; INCOMPLETE" )
        dhcpCfgLofD.appendConfigDict(ConfigDict(dct))
    else:
        logger.debugf("initMyCfgDict::Updating existing master")
        _updateDct(master.getDict(), hostName, activeNIF, "Master: Updated Table" )

    logger.debugf("{}".format(dhcpCfgLofD.toJsonStr()))
    return

above are the original routines
"""

###
####################################################################
