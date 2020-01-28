""" pFlask/main.py Master Raspberry Pi """
#import json
import logging
import sys
#import uuid
#import time
from gevent import monkey
monkey.patch_all()
from flask import Flask         #, render_template, Response, request, url_for
#from flask_bootstrap import Bootstrap
#from flask_debugtoolbar import DebugToolbarExtension
#from flask_googlemaps import GoogleMaps, Map
#from flask_mqtt import Mqtt
from flask_socketio import SocketIO         #, emit, send
#print("sys.path=", sys.path)
try:
    sys.path.append('../common')
    import Constants
except ImportError:
    sys.path.append('/home/pi/raspberry20/common')
    import Constants
#import Configuration
from ActiveNIF import ActiveNIF
from Configuration import ConfigDict, ConfigListOfDict
from HostName import HostName
from MyMqtt import MyMqtt
from LogAllOn import LogAllOn
#from LogAllOff import LogAllOff
#from LogF import LogF
#from LogS import LogS
import SysLog
from TopicMaker import TopicMaker
#from Utilities import Utilities

###################################################################################
###################################################################################
###################################################################################
###################################################################################

def initSysLog(fname):
    """ docstring """
    syslog = SysLog.initialize(__name__, fname, "%(asctime)s — %(name)s — %(levelname)s — %(message)s", logging.DEBUG)
    syslog = LogAllOn(syslog)
    #syslog = LogAllOff(syslog)
    #syslog = LogF(syslog)
    #syslog = LogS(syslog)
    syslog = SysLog.setLogger(syslog)
    syslog.info("Log Started")
    return syslog

def initConfig(pth, fname):
    """ docstring """
    ConfigListOfDict.readConfigFile(pth, fname)
    return

def debugWriteConfigFile(pth, fname):
    """ docstring """
    ConfigListOfDict.getInstance().writeConfigFile(pth, fname)
    return

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

LOG_FNAME = 'dhcp.log'

logger = initSysLog(LOG_FNAME)

activeNIF = ActiveNIF()

hostName = HostName()

mySysType = Constants.CFG_VALUE_SYS_TYPE_DHCP

_dhcpTopicMaker = TopicMaker(activeNIF.getMacAddrAsHexStr())

initConfig(Constants.CFG_FILE_PATH, Constants.CFG_FILE_NAME_DHCP)

ConfigListOfDict.getInstance().updateMyCfgDict(hostName, activeNIF, Constants.CFG_VALUE_SYS_TYPE_DHCP)

def debugWriteConfigFileUpd(fname):
    debugWriteConfigFile(Constants.CFG_FILE_PATH, fname + '.upd')
    return

debugWriteConfigFileUpd(Constants.CFG_FILE_NAME_DEBUG_DHCP)

###################################################################################
####
###################################################################################

#myMacAddr = hex(uuid.getnode())         # hex returns a string

app = Flask(__name__)

app.debug = True
app.env = 'development'
app.secret_key = 'development key'


###################################################################################
####
###################################################################################


app.config['SECRET'] = 'dhcp secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = ConfigListOfDict.getInstance().getIpAddrBroker()
app.config['MQTT_BROKER_PORT'] = ConfigListOfDict.getInstance().getPortBroker(activeNIF.getMacAddrAsHexStr(), mySysType)
app.config['MQTT_CLIENT_ID'] = ''
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 120
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_LAST_WILL_TOPIC'] = 'home/lastwill'
app.config['MQTT_LAST_WILL_MESSAGE'] = ConfigListOfDict.getInstance().getIpAddrBroker() +' disconnect'
app.config['MQTT_LAST_WILL_QOS'] = 2

mqtt = MyMqtt(app)


###################################################################################
####
###################################################################################

# def buildDhcpRsp(reqMacAddr):
#     """
#         Determine system type of requestor from the configuration and create a 
#         customized response specific to the requestor.  

#         If the requestor is a master, return all slaves with that system as their 
#         master

#         If the requestor is a slave, return the master for it
#     """

#     sysDict = dhcpConfigLofD.findEntryForMacAddr(reqMacAddr)

#     if sysDict is None:
#         logger.debugf('No match for MacAddr >%s<', reqMacAddr)
#         return None

#     logger.debugf('Match %s', sysDict)

#     sysType = sysDict.getSysType()

#     if sysType == Constants.CFG_VALUE_SYS_TYPE_MASTER :
#         slaves = dhcpConfigLofD.findAllMatchingEntries(Constants.CFG_VALUE_SYS_TYPE_SLAVE, reqMacAddr)
#         logger.debugf('Matching Slaves %s', slaves)
#         return slaves 

#     return sysDict.getDict()


###################################################################################
####
###################################################################################

@mqtt.on_connect()
def on_connect(client, userdata, flags, rc):
    """ We have connected to the broker, set up our subscriptions and publications """


    logger.debugf("on_connect BEGIN")
    logger.debugf("ID=%s= U=%s= Flgs=%s= RC=%s=" % (client._client_id, userdata, flags, rc))

    topic = TopicMaker.makeTopicDhcpAllReq()

    dhcpCfgDct = ConfigListOfDict.getInstance().findDhcpConfigDict()

    dhcpCfgDct.setMqSub(Constants.CFG_VALUE_DEFAULT_CONNECT)

    dhcpCfgDct.setMqPub(topic)

    jsonStr = ConfigListOfDict.getInstance().toJsonStr()
    
    logger.debugf("Publish %s PyLd: %s" % (topic, jsonStr))

    mqtt.publish(topic, payload=jsonStr, qos=0, retain=False)

    mqtt.subscribe(TopicMaker.makeTopicDhcpAllRsp())

    mqtt.subscribe(TopicMaker.makeTopicDhcpReq())

    logger.debugf("on_connect END")

    return

###################################################################################
####
###################################################################################

def updateLocalDhcpRecordWithRemoteData(mqttMessage):

    logger.debugf("updateLocalDhcpRecordWithRemoteData BEGIN")

    sstr = mqttMessage.payload.decode()  # convert from binary to string

    remoteDhcpDict = ConfigDict.fromJsonStr(sstr)

    localCfgDict = ConfigListOfDict.getInstance().updateCfgDct(remoteDhcpDict)

    if not localCfgDict:
        ConfigListOfDict.getInstance().appendConfigDict(remoteDhcpDict)
        localCfgDict = remoteDhcpDict

    localCfgDict.setMsgLast()

    debugWriteConfigFileUpd(Constants.CFG_FILE_NAME_DEBUG_DHCP)

    logger.debugf("msgPLd=%s=" % localCfgDict)

    logger.debugf("updateLocalDhcpRecordWithRemoteData END")

    return localCfgDict

###################################################################################
####
###################################################################################

""" master subscribes to """
""" slave publishes """

onTopic = TopicMaker.makeTopicDhcpAllRsp()
@mqtt.on_topic(onTopic)
def on_topicDhcpAllRsp(client, userdata, mqttMessage):
    """
        mqttMessage.payload contains a json string
        userdata is data we provided; believe we provide it at time we created the client,
            or when setting up the callback or issuing the command (NEED TO CONFIRM THIS)
    """
    logger.debugf("on_topic(%s) BEGIN" % onTopic)

    localCfgDict = updateLocalDhcpRecordWithRemoteData(mqttMessage)

    if localCfgDict:
        localCfgDict.setMqPub(onTopic)

    logger.debugf("on_topic(%s) END" % onTopic)

    return

###################################################################################
####
###################################################################################

""" master subscribes to """
""" slave publishes """

onTopic = TopicMaker.makeTopicDhcpReq()
@mqtt.on_topic(onTopic)
def on_topicDhcpReq(client, userdata, mqttMessage):

    logger.debugf("on_topic(%s) BEGIN" % onTopic)

    localCfgDict = updateLocalDhcpRecordWithRemoteData(mqttMessage)

    rspTopicMkr = TopicMaker(localCfgDict.getMacAddrSelf())

    rspTopic = rspTopicMkr.makeTopicDhcpRsp()

    #localCfgDict.setMqPub(rspTopic)

    dhcpCfgDct = ConfigListOfDict.getInstance().findDhcpConfigDict()

    dhcpCfgDct.setMqPub(rspTopic)

    jsonStr = ConfigListOfDict.getInstance().toJsonStr()

    logger.debugf("Publish %s" % jsonStr)

    mqtt.publish(rspTopic, payload=jsonStr, qos=0, retain=False)

    logger.debugf("on_topic(%s) END" % onTopic)

    return

###################################################################################
####
###################################################################################

if __name__ == "__main__":
    logger.debugf("Main Begin")

    #global dhcpConfigDict

    #dhcpConfigDict.test()

    #jstr = json.dumps(dhcpConfigDict.getDict(), indent=4, separators=(',', ':'))
    #logger.debugf('dhcpConfigDict=%s' % jstr)

    #jstr = json.dumps(ConfigListOfDict.getInstance().getList(), indent=4, separators=(',', ':'))
    #logger.debugf('CLD=%s' % jstr)

    #brokerIp = dhcpConfigDict.getIpAddrBroker()
    #logger.debugf("broker IP >%s<" % brokerIp)
    
    logger.infof("%s, %s, at MAC addr %s, talking to broker at IP %s port %s" %
                 (hostName.get(), mySysType, activeNIF.getMacAddrAsHexStr(),
                  app.config['MQTT_BROKER_URL'], app.config['MQTT_BROKER_PORT']))

    socketio = SocketIO(app, async_mode='gevent')

    #
    # run method, debug parameter
    #
    # If true, python will automatically reload the program when it detects a change
    # in a source file.  When testing and debuging, this is quite convenient; however,
    # it causes the program to run twice at startup
    #
    socketio.run(app, host='0.0.0.0', debug=False)

    logger.debugf("Main End")


###
