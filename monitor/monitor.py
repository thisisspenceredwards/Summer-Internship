""" pFlask/main.py monitor Raspberry Pi """
#import json
import logging
#import random
import sys
#import time
#import uuid
#from decimateFunction import rdp
from gevent import monkey
monkey.patch_all()
from flask import Flask, render_template  # , Response, request, url_for
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
#from flask_googlemaps import GoogleMaps, Map
#from flask_mqtt import Mqtt
from flask_socketio import SocketIO #, emit, send
#print("sys.path=", sys.path)
try:
    sys.path.append('../common')
    import Constants
except ImportError:
    sys.path.append('/home/pi/raspberry20/common')
    import Constants
import SysLog
from ActiveNIF import ActiveNIF
from Configuration import ConfigListOfDict  # , ConfigDict
from HostName import HostName
from LogAllOn import LogAllOn
#from LogAllOff import LogAllOff
#from LogF import LogF
#from LogS import LogS
from MyMqtt import MyMqtt
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
    cld = ConfigListOfDict.readConfigFile(pth, fname)
    return cld

def debugWriteConfigFile(pth, fname):
    """ docstring """
    ConfigListOfDict.getInstance().writeConfigFile(pth, fname)
    return

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

LOG_FNAME = 'monitor.log'

logger = initSysLog(LOG_FNAME)

activeNIF = ActiveNIF()

hostName = HostName()

monitorTopicMaker = TopicMaker(activeNIF.getMacAddrAsHexStr())

initConfig(Constants.CFG_FILE_PATH, Constants.CFG_FILE_NAME_STARTUP)

ConfigListOfDict.getInstance().updateMonitorDict(hostName, activeNIF)

def debugWriteConfigFileUpd(fname):
    debugWriteConfigFile(Constants.CFG_FILE_PATH, fname + '.upd')
    return

debugWriteConfigFileUpd(Constants.CFG_FILE_NAME_DEBUG_MONITOR)

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

app = Flask(__name__)

app.debug = True
app.env = 'development'
app.secret_key = 'development key'

toolbar = DebugToolbarExtension(app)

app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = False

app.config['MQTT_BROKER_URL'] = ConfigListOfDict.getInstance().getIpAddrBroker()
app.config['MQTT_BROKER_PORT'] = ConfigListOfDict.getInstance().getPortBroker(activeNIF.getMacAddrAsHexStr(), Constants.CFG_VALUE_SYS_TYPE_MONITOR)

app.config['MQTT_CLIENT_ID'] = ''
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''

#app.config['MQTT_PASSWORD'] = '$6$7QORpIqfwTYd+bPI$lDpPacWdaNQl7FMsp5EGgsCmgHhXcpAd6GluzW+0x2ub9uXfnWo8jrfQXo/zjVMPm2o3Gd7UFAB5cZstIeROCA=='

app.config['MQTT_KEEPALIVE'] = 120
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_LAST_WILL_TOPIC'] = 'home/lastwill'
app.config['MQTT_LAST_WILL_MESSAGE'] = 'bye'
app.config['MQTT_LAST_WILL_QOS'] = 2
app.config['GOOGLEMAPS_KEY'] = "AIzaSyCfO5PY5amy-OzmTLT1FCbLaxQiXhG6puM"

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

Bootstrap(app)
mqtt = MyMqtt(app)      # Mqtt(app)
socketio = SocketIO(app, async_mode='gevent')

@app.route("/")
def renderOverlay():
    logger.debugf("renderOverlay")
    return render_template('index.html')


###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

""" monitor """
@mqtt.on_connect()
def on_connect(client, userdata, flags, rc):
    """ We have connected to the broker, set up our subscriptions and publications """

    logger.debugf("on_connect BEGIN")
    #logger.debugf("ID={}= U={}= Flgs={}= RC={}=".format(client, userdata, flags, rc))
    #logger.debugf("ID={}= U={}= Flgs={}= RC={}=".format(client._client_id, userdata, flags, rc))

    mqtt.subscribe(TopicMaker.makeTopicSubscribeAll())
    mqtt.subscribe(TopicMaker.makeTopicDhcpAllReq())
    mqtt.subscribe(monitorTopicMaker.makeTopicDhcpRsp())

    myMacAddr = activeNIF.getMacAddrAsHexStr()
    cfgDict = ConfigListOfDict.getInstance().findMonitorConfigDict(myMacAddr)
    topic = TopicMaker.makeTopicDhcpReq()
    cfgDict.setMqPub(topic)
    cfgDict.setMqSub(Constants.CFG_VALUE_DEFAULT_CONNECT)
    cfgDict.setMsgLast()

    jstr = cfgDict.toJsonStr()
    ret = mqtt.publish(topic, payload=jstr, qos=0, retain=False)

    logger.debugf("Sending DHCP REQ with Record %s", jstr)
    logger.debugf("Ret::%s", ret)

    logger.debugf("on_connect END")

    return


###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

def newDhcpTable(message):

    logger.debugf("newDhcpTable BEGIN")

    jstr = message.payload.decode()

    logger.debugf("Msg=%s=", jstr)

    ConfigListOfDict.fromJsonStr(jstr) #start using the new DHCP table

    ConfigListOfDict.getInstance().updateMyCfgDict(hostName, activeNIF, Constants.CFG_VALUE_SYS_TYPE_MONITOR)

    debugWriteConfigFileUpd(Constants.CFG_FILE_NAME_DEBUG_MONITOR)

    logger.debugf("newDhcpTable END")

    return


""" monitor publishes """
""" slave subscribes to """

@mqtt.on_topic(TopicMaker.makeTopicDhcpAllReq())
def on_topicDhcpAllReq(client, userdata, message):
    """ docstring"""

    on_topic_str = TopicMaker.makeTopicDhcpAllReq()

    logger.debugf("on_topic(%s) BEGIN", on_topic_str)
    
    newDhcpTable(message)

    cfgDict = ConfigListOfDict.getInstance().findMonitorConfigDict(activeNIF.getMacAddrAsHexStr())

    cfgDict.setMsgLast()

    jstr = cfgDict.toJsonStr()
    
    ret = mqtt.publish(TopicMaker.makeTopicDhcpAllRsp(), payload=jstr, qos=0, retain=False)

    logger.debugf("Sending updated cfgDct: %s", jstr)

    logger.debugf("Ret::%s", ret)

    logger.debugf("on_topic(%s) END", on_topic_str)

    return


""" monitor publishes """
""" slave subscribes """

logger.debugf("on_topicDhcpRsp==%s" % monitorTopicMaker.makeTopicDhcpRsp())

@mqtt.on_topic(monitorTopicMaker.makeTopicDhcpRsp())
def on_topicDhcpRsp(client, userdata, message):
    """
        We have rcvd a DHCP RSP with a new DHCP Config
        Update our copy of the DHCP Config
        Update our entry in the table
        Update all local copies, if any, of entries in the table
    """
    on_Topic_str = monitorTopicMaker.makeTopicDhcpRsp()

    logger.debugf("on_topic(%s) BEGIN", on_Topic_str)

    newDhcpTable(message)

    logger.debugf("on_topic(%s) END", on_Topic_str)

    return


""" monitor subscribes to """
""" slave publishes """

@mqtt.on_topic(monitorTopicMaker.makeTopicCmdRsp())
def on_topicCmdRsp(client, userdata, message):
    """ Docstring """
    on_topic_str = monitorTopicMaker.makeTopicCmdRsp()

    logger.debugf("on_topic(%s) BEGIN", on_topic_str)
    #logger.debugf("ID={}= U={}= Msg={}=".format(client, userdata, message))

    jstr = message.payload.decode()
    logger.debugf("msg.topic={}= payload={}= qos={}=".format(message.topic, jstr, message.qos))

    logger.debugf("on_topic(%s) END", on_topic_str)



@mqtt.on_topic(monitorTopicMaker.makeTopicMisc())
def on_topicMisc(client, userdata, message):
    """ Docstring """
    on_topic_str = monitorTopicMaker.makeTopicMisc()
    logger.debugf("on_topic(%s) BEGIN", on_topic_str)
    #logger.debugf("ID={}= U={}= Msg={}=".format(client, userdata, message))

    jstr = message.payload.decode()
    logger.debugf("msg.topic=%s= payload=%s= qos=%s=", message.topic, jstr, message.qos)

    logger.debugf("on_topic(%s) END", on_topic_str)


"""
    on_publish
    the publish callback
    This confirms that a specific message was published
        mid:    message ID of the published message 
"""
@mqtt.on_publish()
def handle_mqtt_publish(client, userdata, mid):
    """ Docstring """
    logger.debugf('Published message with mid %d', mid)
    logger.debugf("on_publish() END")


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    #logger.debugf("handle_mqtt_message BEGIN")
    logger.debugf(">%s<  >%s<" % (message.topic, message.payload.decode()))
    #logger.debugf("handle_mqtt_message END")


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    """ Docstring """
    logger.debugf("ID=%s= U=%s= Lvl=%s= buf=%s=", client, userdata, level, buf)


@mqtt.on_disconnect()
def handle_disconnect():
    """ Docstring """
    logger.debugf('handle_disconnect BEGIN')
    logger.debugf("handle_disconnect END")



"""
    Standard mainline.  No attempt to capture CTRL-C or to cleanup sessions
"""

if __name__ == '__main__':
    # host=ip Addr or host name to listen on

    listenIpAddr = activeNIF.getIpAddr()

    macAddr = activeNIF.getMacAddrAsHexStr()

    httpPort = ConfigListOfDict.getInstance().getPortHttp(macAddr, Constants.CFG_VALUE_SYS_TYPE_MONITOR)

    logger.infof("%s, monitor, at MAC addr %s, listening on Host/IP %s port %s",
                 hostName.get(), macAddr, listenIpAddr, httpPort)

    #
    # run method, debug parameter
    #
    # If true, python will automatically reload the program when it detects a change
    # in a source file.  When testing and debuging, this is quite convenient; however,
    # it causes the program to run twice at startup
    #
    try:
        socketio.run(app, host=listenIpAddr, port=httpPort, debug=False)
    except Exception as e:
        socketio.run(app, host='0.0.0.0', port=0, debug=False)

#"""
#"""
