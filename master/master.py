""" pFlask/main.py Master Raspberry Pi """
import json
import logging
import random
import sys
#import time
#import uuid
from gevent import monkey
monkey.patch_all()
from flask import Flask, render_template  # , Response, request, url_for
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from flask_socketio import SocketIO #, emit, send
from flask_googlemaps import GoogleMaps, Map
#from flask_mqtt import Mqtt
from decimateFunction import rdp
#print("sys.path=", sys.path)
try:
    sys.path.append('../common')
    import Constants
except ImportError:
    sys.path.append('/home/pi/raspberry20/common')
    import Constants
import SysLog
from ActiveNIF import ActiveNIF
from Configuration import ConfigDict, ConfigListOfDict
from HostName import HostName
from LogAllOn import LogAllOn
#from LogAllOff import LogAllOff
#from LogF import LogF
#from LogS import LogS
from MyMqtt import MyMqtt
from TopicMaker import TopicMaker
#from Utilities import Utilities

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

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

LOG_FNAME = 'master.log'

logger = initSysLog(LOG_FNAME)

activeNIF = ActiveNIF()

hostName = HostName()

mySysType = Constants.CFG_VALUE_SYS_TYPE_MASTER

masterTopicMaker = TopicMaker(activeNIF.getMacAddrAsHexStr())

initConfig(Constants.CFG_FILE_PATH, Constants.CFG_FILE_NAME_STARTUP)

ConfigListOfDict.getInstance().updateMyCfgDict(hostName, activeNIF, mySysType)

def debugWriteConfigFileUpd(fname):
    debugWriteConfigFile(Constants.CFG_FILE_PATH, fname + '.upd')
    return

debugWriteConfigFileUpd(Constants.CFG_FILE_NAME_DEBUG_MASTER)

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
app.config['MQTT_BROKER_PORT'] = ConfigListOfDict.getInstance().getPortBroker(activeNIF.getMacAddrAsHexStr(), Constants.CFG_VALUE_SYS_TYPE_MASTER)

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

#
# Use a list of dictionaries to hold connected raspberries
#
# Each list entry is unique, and is identified by it's MAC address.
# Searching the list by MAC address will return a dictionary of
# key,value pairs for the rPi at that MAC address
#

#
#raspberryList = {'38.1644611,-120.9582994',
#                 '38.1645265,-120.9582942' }

# 38.164525, -120.958005
# 38.164458, -120.958002

# When included in dictionary, infobox is used by google maps to make infobox
#'infobox': "<b>Hello World</b>"    # for the raspberry
#'infobox': "<b>Hello World from other place</b>"

# theRaspberriesList = [
#     {
#         'icon': 'http://maps.google.com/mapfiles/kml/paddle/red-circle.png',
#         'lat': '38.0040558',
#         'lng': '-121.8755571',                   # storing & retrieving floats leads to discrepancies in the numbers
#         'title' : '38.0040558,-121.8755571'      # using title to pass the unaltered lat & longitude for making the URL 
#         #'infobox': "<b>Hello World</b>"         # for the raspberry
#     },
#     {
#         'icon': 'http://maps.google.com/mapfiles/kml/paddle/blu-circle.png',
#         'lat': '38.1645265',
#         'lng': '-120.9582942',
#         'title' : '38.1645265,-120.9582942'
#         #'infobox': "<b>Hello World from other place</b>"
#     }
# ] 

# theRaspberriesList.append({
#     'MAC' : '123456789ABC',
#     'icon': Constants.ICON_GREEN_DOT,
#     'lat': '38.164525',                 # Store floats as strings to prevent float creep
#     'lng': '-120.958005',               # Storing & retrieving floats leads to discrepancies in the numbers
#     'title' : '38.1638,-120.9582892'    # Using title to pass the unaltered lat & longitude for making the URL
#     })

# theRaspberriesList.append({
#     'MAC' : 'ABCDEF123456',
#     'icon': Constants.ICON_BLUE_DOT,
#     'lat': '38.164458',
#     'lng': '-120.958002',
#     'title' : '38.1644,-120.9582850'
#     })

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

Bootstrap(app)
mqtt = MyMqtt(app)      # Mqtt(app)
socketio = SocketIO(app, async_mode='gevent')
GoogleMaps(app)         #, key="AIzaSyCfO5PY5amy-OzmTLT1FCbLaxQiXhG6puM")

_mapData = ""
def setMapData(md):
    global _mapData
    _mapData = md

#mqtt.message_callback_add('111', 'callback')
#mqtt.message_callback_remove('111')

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
@app.route("/line")
def line():
    return render_template("svgLine.html")



@app.route("/mac")
def mac():
    macList=[]
    macAddresses = ConfigListOfDict.getInstance().findAllSlavesForMaster(activeNIF.getMacAddrAsHexStr())
    for i in macAddresses:
        macList.append(i.getMacAddrSelf())
    return render_template("mac.html", macList=macList)


def makeCollectionOfSlavesForMap():
    logger.debugf('makeCollectionOfSlavesForMap BEGIN')
    lslaves = []     #list of dictionaries
    configSlaves = ConfigListOfDict.getInstance().findAllSlavesForMaster(activeNIF.getMacAddrAsHexStr())
    for cfgDict in configSlaves:
        dct = cfgDict.getDict()
        dslave={}
        dslave[Constants.CFG_KEY_ICON]     = dct[Constants.CFG_KEY_ICON]
        dslave[Constants.CFG_KEY_LAT]      = dct[Constants.CFG_KEY_LAT]
        dslave[Constants.CFG_KEY_LNG]      = dct[Constants.CFG_KEY_LNG]
        dslave[Constants.CFG_KEY_MAC_SELF] = dct[Constants.CFG_KEY_MAC_SELF]
        dslave[Constants.CFG_KEY_TITLE]    = dct[Constants.CFG_KEY_TITLE]
        lslaves.append(dslave)
    jstr = json.dumps(lslaves, indent=4, separators=(',', ':'))
    logger.debugf("All matching slaves: %s" % jstr)
    logger.debugf('makeCollectionOfSlavesForMap END')
    return lslaves


@app.route("/googlemaps", methods=['GET', 'POST'])
def mapview():
    logger.debugf("app.route(/googlemaps) mapview BEGIN")
    lslaves = makeCollectionOfSlavesForMap()
    mymap = Map(
        identifier="view-side",
        varname="mymap",
        lat=38.1644611,
        lng=-120.9582994,
        maptype='SATELLITE',
        style="position:absolute;height:100vh;width:100%;margin:0px;border-width:2px;border-style:solid;border-color:black;",  # default is ==> style="$
        zoom=20,
        markers=lslaves,
        collapsible=False,
        maptype_control=True,
        streetview_control=False,
        fullscreen_control=False
    )
    logger.debugf("app.route(/googlemaps) mapview END")
    return render_template('googlemaps.html', mymap=mymap)


@app.route("/user")
def userA():
    logger.debugf("app.route(user)/userA")
    return render_template('user.html')


@app.route("/picture")
def renderPicture():
    logger.debugf("renderPicture()/picture")
    return render_template('picture.html')


@app.route("/")
def renderOverlay():
    logger.debugf("renderOverlay")
    return render_template('index.html')

@app.route("/chart")
def graph():
    logger.debugf("app.route(chart)/graph BEGIN")
    rawTime = {}
    rawValues = []
    smashedData = []
    unalteredData = []
    unalteredValues = []
    alteredKeys = []
    alteredValues = []
    unalteredKeys = []
    unalteredValues = []
    index = 0
    for x in range(1,13):
        for y in range(0, 60, 1):
            time = ("%0*d" % (2, x)) + ":" + ("%0*d" % (2, y)) + ":" + '00'
            rNumber = random.normalvariate(7, 1)
            rawTime.update({index: time})
            rawValues.append((index, rNumber))
            index = index + 1
    unalteredData= dict(rawValues)
    smashedData = (rdp(rawValues, 1))
    dictSmashedData = dict(smashedData)
    for y in dictSmashedData:
        alteredKeys.append(rawTime[y])
        alteredValues.append(dictSmashedData[y])
    for y in unalteredData:
        unalteredKeys.append(rawTime[y])
        unalteredValues.append(unalteredData[y])
    logger.debugf("this is original length %d" % len(rawValues))
    #logger.debugf(rawValues)
    logger.debugf("This is final length %d" % len(alteredKeys))
    #logger.debugf(alteredValues)
    logger.debugf("app.route(chart)/graph END")
    return render_template('chart.html', alteredKeys=alteredKeys, alteredValues=alteredValues, unalteredKeys=unalteredKeys, unalteredValues=unalteredValues )



@app.route("/<raspberry>") # methods=['GET','POST'])
def fraspberry(raspberry):
    logger.debugf("fraspberry(raspberry)")
    return render_template('raspberry.html', raspberry = raspberry)


@socketio.on('initalizeMap')
def handle_map(data):
    logger.debugf('socketio initalizeMap BEGIN')
    logger.debugf(data)
    setMapData(data)
    logger.debugf('socketio initalizeMap END')


@socketio.on('publish')
def handle_publish(json_str):
    """
        Translate from SocketIO to MQTT and pass the message thru to whoever
        subscribes to the MQTT topic.  This is how the slave can receive
        messages that originated from the front end (the browser)

        As of July 30, 2019 --
            topic   == the slave's MAC address
            message == the command as a string 
            qos     == ???
    """
    logger.debugf("socketio publish BEGIN")
    data = json.loads(json_str)
    ret = mqtt.publish(data['topic'], data['message'], data['qos'])
    logger.debugf('topic %s msg %s qos %d' % (data['topic'], data['message'], data['qos']))
    logger.debugf("Ret:%d mid:%d" % ret)
    logger.debugf("socketio publish END")


@socketio.on('subscribe')
def handle_subscribe(json_str):
    logger.debugf("socketio handle_subscribe BEGIN")
    logger.debugf("json %s" % json_str)
    data = json.loads(json_str)
    mqtt.subscribe(data['topic'], data['qos'])
    logger.debugf("socketio handle_subscribe END")


@socketio.on('sendMessage')
def handle_message(json_str):
    """
        Translate from SocketIO to MQTT and pass the message thru to whoever
        subscribes to the MQTT topic.  This is how the slave can receive
        messages that originated from the front end (the browser)

        As of July 30, 2019 --
            topic   == the slave's MAC address
            message == the command as a string 
            qos     == ???
    """
    logger.debugf("socketio handle_message BEGIN")
    logger.debugf("json %s" % json_str)
    data = json.loads(json_str)
    ret = mqtt.publish(data['topic'], data['message'], data['qos'])
    logger.debugf("Ret:%d mid:%d" % ret)
    logger.debugf("socketio handle_message END")

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

def sendSignOnToSlaves():

    logger.debugf("sendSignOnToSlaves BEGIN")

    myMacAddr = activeNIF.getMacAddrAsHexStr()
    slavesLofD = ConfigListOfDict.getInstance().findAllSlavesForMaster(myMacAddr)

    for slvCfg in slavesLofD:
        slvMacAddr = slvCfg.getMacAddrSelf()
        slvTopMkr = TopicMaker(slvMacAddr)
        topic = slvTopMkr.makeTopicSignonReq()
        slvCfg.setMsgLast()
        jstr = slvCfg.toJsonStr()
        ret = mqtt.publish(topic, payload=jstr, qos=0, retain=False)
        logger.debugf("Sending Slave Signon REQ %s" % topic)
        logger.debugf("Ret:%d mid:%d" % ret)

    logger.debugf("sendSignOnToSlaves END")
    return


""" MASTER """
@mqtt.on_connect()
def on_connect(client, userdata, flags, rc):
    """ We have connected to the broker, set up our subscriptions and publications """

    logger.debugf("on_connect BEGIN")
    #logger.debugf("ID={}= U={}= Flgs={}= RC={}=".format(client, userdata, flags, rc))
    #logger.debugf("ID={}= U={}= Flgs={}= RC={}=".format(client._client_id, userdata, flags, rc))

    mqtt.subscribe('initialize', 2)
    mqtt.subscribe('pushNotification')
    #mqtt.subscribe('altitude')
    mqtt.publish('subscriber', 'connectToPublisher', 2)

    mqtt.subscribe(masterTopicMaker.makeTopicDhcpAllReq())
    mqtt.subscribe(masterTopicMaker.makeTopicDhcpRsp())

    mqtt.subscribe(masterTopicMaker.makeTopicSignonRsp())
    mqtt.subscribe(masterTopicMaker.makeTopicCmdRsp())

    myMacAddr = activeNIF.getMacAddrAsHexStr()
    cfgDict = ConfigListOfDict.getInstance().findMasterConfigDict(myMacAddr)
    topic = masterTopicMaker.makeTopicDhcpReq()
    cfgDict.setMqPub(topic)
    cfgDict.setMqSub(Constants.CFG_VALUE_DEFAULT_CONNECT)
    cfgDict.setMsgLast()

    jstr = cfgDict.toJsonStr()
    ret = mqtt.publish(topic, payload=jstr, qos=0, retain=False)

    logger.debugf("Sending DHCP REQ with Record %s" % jstr)
    logger.debugf("Ret:%d mid:%d" % ret)

    sendSignOnToSlaves()

    logger.debugf("on_connect END")

    return


@mqtt.on_topic('initialize')
def initialize(client, userdata, message):
    logger.debugf("mqtt.on_topic(initialize) BEGIN")
    #logger.debugf('client %s userdata %s message %s', client, userdata, message)
    sstr = message.payload.decode()
    logger.debugf('topic %s mssg %s qos %d', message.topic, sstr, message.qos)
    #messageList = sstr.split(" ", 1)
    #logger.debugf("mlst[0]=%s mlst[1]=%s", messageList[0], messageList[1])
    #if messageList[0] not in raspberryList:
    #   print("not in list")
    #   raspberryList[messageList[0]]= messageList[1]
    logger.debugf("mqtt.on_topic(initialize) END")
    return


@mqtt.on_topic('altitude')
def on_altitude(client, userdata, message):
    logger.debugf("@mqtt.on_topic(altitude) BEGIN")
    sdata = message.payload.decode()
    logger.debugf("msg payload %s" % sdata)
    socketio.emit('altitudeJs', sdata)   #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    logger.debugf("@mqtt.on_topic(altitude) END")


# @mqtt.on_topic('pushNotification')
# def on_pushNotification(client, userdata, message):
#     print('PUSH NOTIFICATION')
#     print('client', client)
#     print('userdata', userdata)
#     print('message', message)
#     print('message decode', message.payload.decode())
#     print('message.topic', message.topic)
#     print('message.qos', message.qos)
#     messageList = message.payload.decode()
#     print(messageList, 'messageList')
# #    print(messageList[1], 'messageList1')
#     print("INITIALIZE CALLED")
#     socketio.emit('pushNotification', 'Last Message Recieved: ' + messageList)  
#     print("pushnotication socketio")

@mqtt.on_topic('pushNotification')
def on_pushNotification(client, userdata, message):
    logger.debugf('PUSH NOTIFICATION BEGIN')
    #logger.debugf('client %s userdata %s message %s' % (client, userdata, message))
    sdata = message.payload.decode()
    socketio.emit('Last Message Recieved: ')  
    logger.debugf('topic %s data %s qos %d' % (message.topic, sdata, message.qos))
    logger.debugf('PUSH NOTIFICATION END')


###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

def newDhcpTable(message):

    logger.debugf("newDhcpTable BEGIN")

    jstr = message.payload.decode()

    logger.debugf("Msg=%s=" % jstr)

    dclofd = ConfigListOfDict.fromJsonStr(jstr) #start using the new DHCP table

    dclofd.updateMyCfgDict(hostName, activeNIF, mySysType)

    debugWriteConfigFileUpd(Constants.CFG_FILE_NAME_DEBUG_MASTER)

    sendSignOnToSlaves()

    logger.debugf("newDhcpTable END")

    return


def updateSlaveConfigDict(message):

    logger.debugf("newSlaveConfigDict BEGIN")

    jstr = message.payload.decode()

    logger.debugf("Msg=%s=" % jstr)

    rmtDct = ConfigDict.fromJsonStr(jstr)

    lclDct = ConfigListOfDict.getInstance().updateCfgDct(rmtDct)

    if not lclDct:
        ConfigListOfDict.getInstance().addConfigDict(rmtDct)
        rmtDct.setMsgLast()

    debugWriteConfigFileUpd(Constants.CFG_FILE_NAME_DEBUG_MASTER)

    logger.debugf("newSlaveConfigDict END")
    return


""" master publishes """
""" slave subscribes to """

@mqtt.on_topic(TopicMaker.makeTopicDhcpAllReq())
def on_topicDhcpAllReq(client, userdata, message):
    """ docstring"""

    on_topic_str = TopicMaker.makeTopicDhcpAllReq()

    logger.debugf("on_topic(%s) BEGIN" % on_topic_str)
    
    newDhcpTable(message)

    cfgDict = ConfigListOfDict.getInstance().findMasterConfigDict(activeNIF.getMacAddrAsHexStr())

    cfgDict.setMsgLast()

    jstr = cfgDict.toJsonStr()
    
    ret = mqtt.publish(TopicMaker.makeTopicDhcpAllRsp(), payload=jstr, qos=0, retain=False)

    logger.debugf("Sending updated cfgDct: %s" % jstr)

    logger.debugf("Ret:%d mid:%d" % ret)

    logger.debugf("on_topic(%s) END" % on_topic_str)

    return


""" master publishes """
""" slave subscribes """

@mqtt.on_topic(masterTopicMaker.makeTopicDhcpRsp())
def on_topicDhcpRsp(client, userdata, message):
    """
        We have rcvd a DHCP RSP with a new DHCP Config
        Update our copy of the DHCP Config
        Update our entry in the table
        Update all local copies, if any, of entries in the table
    """
    on_Topic_str = masterTopicMaker.makeTopicDhcpRsp()

    logger.debugf("on_topic(%s) BEGIN" % on_Topic_str)

    newDhcpTable(message)

    logger.debugf("on_topic(%s) END" % on_Topic_str)

    return


#""" master subscribes to """
#""" slave publishes """
# @mqtt.on_topic(Constants.RACK_TOPIC_DHCP_REQ)
# def on_topicDhcpReq(client, userdata, message):
#     """ Docstring """
#     logger.debugf("on_topic({}) BEGIN".format(Constants.RACK_TOPIC_DHCP_REQ))
#     logger.debugf("ID={}= U={}= Msg={}=".format(client, userdata, message))

#     messagePayloadList = message.payload.decode()
#     logger.debugf("msg.topic={}= payload={}= qos={}=".format(message.topic, messagePayloadList, message.qos))

#     str = json.dumps(debugDhcp)
#     logger.debugf('dhcp dict (JSON str): >{}<'.format(str))

#     mqtt.publish(Constants.RACK_TOPIC_DHCP_RSP, payload=str, qos=0, retain=False)

#     logger.debugf("on_{} END".format(Constants.RACK_TOPIC_DHCP_REQ))


""" master subscribes to """
""" slave publishes """
@mqtt.on_topic(masterTopicMaker.makeTopicSignonRsp())
def on_topicSlaveSignonRsp(client, userdata, message):
    """ Docstring """
    on_topic_str = masterTopicMaker.makeTopicSignonRsp()

    logger.debugf("on_topic(%s) BEGIN" % on_topic_str)

    updateSlaveConfigDict(message)

    logger.debugf("on_topic(%s) END" % on_topic_str)

    return



    # message = message.payload.decode()
    # logger.debugf("msg.topic=%s= payload=%s= qos=%s=", message.topic, message, message.qos)

    # timestampstr = Utilities.getTimeStampSecsAsStr()

    #     #
    #     # use a generator expression to search thru an enumeration of the list of raspberries
    #     # for the existing entry with matching MAC address
    #     # if found return the index in the list, otherwise return the default value None
    #     #
    # index = (next((i for i, item in enumerate(theRaspberriesList) if item["MAC"] == macAddr), None))

    # if index is None:
    #     print('rPi NEW')
    #     temp = gps.split(',')
    #     #DEBUG ** fle ** todo::fix this
    #     rPi = {'MAC' : macAddr, 'GPS' : gps, 'MsgFirst' : timestampstr, 'icon' : Constants.ICON_GREEN_DOT, 'lat' : temp[0], 'lng' : temp[1], 'title' : gps}
    #     theRaspberriesList.append(rPi)
    # else:
    #     print('rPi FOUND')
    #     rPi = theRaspberriesList[index]

    # rPi['MsgLatest'] = timestampstr

    # logger.debugf("rPi={}".format(rPi))

    # logger.debugf('theRaspberriesList={}'.format(theRaspberriesList))

    # logger.debugf("on_{} END".format(Configuration.makeTopicSignonRsp(activeNIF.getMacAddrAsHexStr())))

    # return


""" master subscribes to """
""" slave publishes """

@mqtt.on_topic(masterTopicMaker.makeTopicCmdRsp())
def on_topicCmdRsp(client, userdata, message):
    """ Docstring """
    on_topic_str = masterTopicMaker.makeTopicCmdRsp()

    logger.debugf("on_topic(%s) BEGIN" % on_topic_str)
    #logger.debugf("ID={}= U={}= Msg={}=".format(client, userdata, message))

    jstr = message.payload.decode()
    logger.debugf("msg.topic=%s= payload=%s= qos=%d=" % (message.topic, jstr, message.qos))

    logger.debugf("on_topic(%s) END" % on_topic_str)



@mqtt.on_topic(masterTopicMaker.makeTopicMisc())
def on_topicMisc(client, userdata, message):
    """ Docstring """
    on_topic_str = masterTopicMaker.makeTopicMisc()
    logger.debugf("on_topic(%s) BEGIN" % on_topic_str)
    #logger.debugf("ID={}= U={}= Msg={}=".format(client, userdata, message))

    jstr = message.payload.decode()
    logger.debugf("msg.topic=%s= payload=%s= qos=%d=" % (message.topic, jstr, message.qos))

    logger.debugf("on_topic(%s) END" % on_topic_str)


"""
    on_publish
    the publish callback
    This confirms that a specific message was published
        mid:    message ID of the published message 
"""
@mqtt.on_publish()
def handle_mqtt_publish(client, userdata, mid):
    """ Docstring """
    logger.debugf('Published message with mid %d' % mid)
    logger.debugf("on_publish() END")


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    logger.debug("handle mqtt message BEGIN")
    sss = message.payload.decode()
    logger.debug('msg payload: %s' % sss)
    data = dict(
        topic= message.topic,
        payload= sss,
        qos=message.qos,
    )
    socketio.emit('mqtt_message', data=data)
    logger.debug("handle mqtt message END")


# @mqtt.on_message()
# def handle_mqtt_message(client, userdata, message):
#     """ Docstring """
#     logger.debugf("handle_mqtt_message BEGIN")
#     #logger.debugf("ID=%s= U=%s= Msg=%s=", client, userdata, message)

#     jstr = message.payload.decode()
#     logger.debugf("msg.topic=%s= payload=%s= qos=%s=", message.topic, jstr, message.qos)

#     data = dict(
#         topic=message.topic,
#         payload=jstr,
#         qos=message.qos,
#     )
#     socketio.emit('mqtt_message', data=data)
#     logger.debugf("socketio.emit")
#     logger.debugf("handle_mqtt_message END")



@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    """ Docstring """
#   logger.debugf("ID=%s= U=%s= Lvl=%s= buf=%s=", client._client_id, userdata, level, buf)
    logger.debugf("ID=%s= U=%s= Lvl=%s= buf=%s=" % (client, userdata, level, buf))



@mqtt.on_disconnect()
def handle_disconnect():
    """ Docstring """
    logger.debugf('handle_disconnect BEGIN')
    logger.debugf("handle_disconnect END")



###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################


#print("\n********** Main: mqtt.subscribe('$SYS') BEGIN  {}".format(datetime.now()))
#mqtt.subscribe('$SYS/#')
#mqtt.subscribe('root/#')
#mqtt._client.connect()
#print("********** Main: mqtt.subscribe('$SYS') END  {}\n".format(datetime.now()))


"""
CTRL-C handler
    Use this along with signal.signal(signal.SIGINT, signal_handler), below,
    if you want to capture the SIGINT signal
"""
"""
def signal_handler(sig, frame):
        print('CTRL-C')
        mqtt.unsubscribe_all()
        mqtt._disconnect()
        sys.exit(0)
"""

"""
    Uncomment following to capture SIGINT, the CTRL-C KeyboardInterrupt
"""
#signal.signal(signal.SIGINT, signal_handler)



"""
    MQTT will occassionally get into a connect/disconnect infinite loop that
    can only be cured by a reboot of the client and, in the worst cases, the
    broker.

    This seemed to be related to repeated starts and stops from code changes
    with DEBUG enabled, and CTRL-C interrupts to terminate the client.
    I made several attempts to capture CTRL-C and to clean up the state of the
    system and its current sessions.  Nothing seemed to help.

    Found a reference that said good practice was to use exception handling
    to detect keyboardInterrupt.  The code is below.  As before, this did
    not seem to help.

    All in all, my experiments were inconclusive.
"""
"""
if __name__ == '__main__':
    try:
        socketio.run(app, debug=True)
    except KeyboardInterrupt:
        print('>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<')
        print('>>>>>>>>>>>  CTRL-C  <<<<<<<<<<<')
        print('>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<')
        print("Keyboard interrupt.  Stopping …")
    finally:
        print('>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<')
        print('>>>>>>>>    CTRL-C     <<<<<<<<<')
        print('>>>>>>>>  Cleaning Up  <<<<<<<<<')
        print('>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<')
        mqtt.unsubscribe_all()
        mqtt._disconnect()
"""

"""
    Standard mainline.  No attempt to capture CTRL-C or to cleanup sessions
"""

if __name__ == '__main__':
    # host=ip Addr or host name to listen on

    listenIpAddr = activeNIF.getIpAddr()

    macAddr = activeNIF.getMacAddrAsHexStr()

    httpPort = ConfigListOfDict.getInstance().getPortHttp(macAddr, mySysType)
    
    logger.infof("%s, %s, at MAC addr %s, listening on Host/IP %s port %s" %
                 (hostName.get(), mySysType, macAddr, listenIpAddr, httpPort))
    #
    # run method, debug parameter
    #
    # If true, python will automatically reload the program when it detects a change
    # in a source file.  When testing and debuging, this is quite convenient; however,
    # it causes the program to run twice at startup
    #
    socketio.run(app, host=listenIpAddr, port=httpPort, debug=False)

#"""
#"""
