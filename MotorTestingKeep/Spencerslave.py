""" sFlask/main.py Slave Raspberry Pi """
from gevent import monkey
monkey.patch_all()
#import json
import logging
import sys
import threading
import time
#import uuid
from pysolar.solar import *
import pytz
from datetime import datetime, timezone
from flask import Flask, render_template  # , request
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
#from flask_googlemaps import GoogleMaps, Map, icons
#from flask_mqtt import Mqtt
from flask_socketio import SocketIO, emit   #, send


try:
    print("sys.path.append(../common)")
    sys.path.append('../common')
    import Constants
except ImportError:
    print("sys.path.append(/home/pi/raspberry20/common)")
    sys.path.append('/home/pi/raspberry20/common')
    import Constants
#from ActiveNIF import ActiveNIF
#import Configuration
#rom Configuration import ConfigDict, ConfigListOfDict
#import SysLog
#from HostName import HostName
#from LogAllOn import LogAllOn
#from LogAllOff import LogAllOff
#from LogF import LogF
#from LogS import LogS
#from MyMqtt import MyMqtt
#from Utilities import *

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
#
# To comment out the rPi specific code, change comments at beginning and ending
# of comment blocks around the rPi code.
#
# Beginning of Code Block
#
#       Change
#               """ ####@@#GPIO  Enable/Disable GPIO            <<<< Disable GPIO
#       to
#               ### ####@@#GPIO   Enable/Disable GPIO            <<<< Enable GPIO
#
# End of Code Block
#
#       Change 
#               #@@#GPIO#### """                                <<<< Disable GPIO
#       to
#               #@@#GPIO#### ###                                <<<< Enable GPIO
#

### ####@@#GPIO    Enable/Disable GPIO
import RPi.GPIO as GPIO
####GPIO####      Enable/Disable #@@#GPIO#### ###

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

'''LOG_FNAME = 'slave.log'

def initSysLog(fname):
    """ docstring """
    syslog = SysLog.initialize(__name__, fname, "%(asctime)s - %(name)s - %(levelname)s - %(message)s", logging.DEBUG)
    #syslog = LogAllOn(syslog)
    #syslog = LogAllOff(syslog)
    #syslog = LogF(syslog)
    syslog = LogS(syslog)
    syslog = SysLog.setLogger(syslog)
    syslog.info("Log Started")
    return syslog

def initConfig(pth, fname):
    """ docstring """
    cld = ConfigListOfDict.readConfigFile(pth, fname)
    return cld

def debugWriteConfigFile(pth, fname, cld):
    """ docstring """
    cld.writeConfigFile(pth, fname)
    return

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

logger = initSysLog(LOG_FNAME)

activeNIF = ActiveNIF()

hostName = HostName()

slaveTopicMaker = TopicMaker(activeNIF.getMacAddrAsHexStr())

_dhcpConfigLofD = initConfig(Constants.CFG_FILE_PATH, Constants.CFG_FILE_NAME_STARTUP)

_dhcpConfigLofD.updateMyCfgDict(hostName, activeNIF, Constants.CFG_VALUE_SYS_TYPE_SLAVE)

def getDhcpConfigLofD():
    #global _dhcpConfigLofD
    return _dhcpConfigLofD

def debugWriteConfigFileUpd(fname):
    debugWriteConfigFile(Constants.CFG_FILE_PATH, fname + '.upd', getDhcpConfigLofD())
    return

def setDhcpConfigLofD(dclofd):
    logger.debugf("setDhcpConfigLofD BEGIN")
    global _dhcpConfigLofD
    _dhcpConfigLofD = dclofd
    debugWriteConfigFileUpd(Constants.CFG_FILE_NAME_DEBUG_SLAVE)
    logger.debugf("setDhcpConfigLofD END")
    return

debugWriteConfigFileUpd(Constants.CFG_FILE_NAME_DEBUG_SLAVE)
'''
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

cfgTrackSolarON = True
#cfgTrackSolarON = False


#logger.infof("Log Started")


###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

app = Flask(__name__)

app.debug = True
app.env = 'development'
app.secret_key = 'development key'

#toolbar = DebugToolbarExtension(app)

relayWest = 23
relayEast = 22


'''app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = getDhcpConfigLofD().getIpAddrBroker()
app.config['MQTT_BROKER_PORT'] = getDhcpConfigLofD().getPortBroker(activeNIF.getMacAddrAsHexStr(), CFG_VALUE_SYS_TYPE_SLAVE)
app.config['MQTT_CLIENT_ID'] = ''
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 120
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_LAST_WILL_TOPIC'] = 'home/lastwill'
app.config['MQTT_LAST_WILL_MESSAGE'] = activeNIF.getMacAddrAsHexStr() +' disconnect'
app.config['MQTT_LAST_WILL_QOS'] = 2
'''
Bootstrap(app)
#mqtt = MyMqtt(app)
socketio = SocketIO(app, async_mode='gevent')

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
#assorted methods
def setup():
    """ docstring"""
#    logger.debugs("Setup BEGIN")
    ### ####@@#GPIO     Enable/Disable GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    #GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(relayWest, GPIO.OUT)
    GPIO.output(relayWest, GPIO.LOW)
    GPIO.setup(relayEast, GPIO.OUT)
    GPIO.output(relayEast, GPIO.LOW)
    ####GPIO####       Enable/Disable #@@#GPIO#### ###
   # logger.debugs("Setup END")
    return


###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

        # fle::  _ vs __

class ThreadController:
    def __init__(self):
        self.__thread = None
        self.__stop_threads = False

    def start_thread(self, method):
        print("start_thread called")
        self.set_stop_threads(False)
        self._thread = self.get_thread()
        if self.__thread is None:
            self.__thread = threading.Thread(target=method)
            self.__thread.start()
        else:
            return -1

    def stop_threads(self):
        print("stop threads called")
       # logger.debugs("Stop threads called")
        self.set_stop_threads(True)
       # self.set_thread(None)

    def get_thread(self):
        return self.__thread

    def set_thread(self, new):
        self.__thread = new

    def get_stop_threads(self):
        return self.__stop_threads

    def set_stop_threads(self, value):
        self.__stop_threads = value


class SolarThread(ThreadController):
    __instance = None
    __track_solar_on = False
    @staticmethod
    def getInstance():
        if SolarThread.__instance == None:    # fle::
            SolarThread.__instance = SolarThread()
        return SolarThread.__instance

    def __init__(self):
        print("init called")
        if SolarThread.__instance != None:
            raise Exception("Only one Solar Thread allowed")
        else:
            super().__init__()
            #SolarThread.__instance = self       # fle::
            self.__last_recorded_altitude = None
            self.__time_of_last_recorded_altitude = None
            self.__time_thread_started = None
            self.__vertical = None
            self.__horizontal = None
    def trackSolar(self):
        if SolarThread.__track_solar_on == False:
            SolarThread.__track_solar_on = True
        else:
            return -1
        start_time = self.get_time() #time thread started
        last_recorded_altitude = self.__set_last_recorded__altitude(start_time)
        self.__set_time_of_last_recorded_altitude(start_time)
        while True:
            print("trackSolar")
            sstop_threads = super().get_stop_threads()
            print("this is sstop threads")
            print(sstop_threads)
           # logger.debugs("this is stop_threads")
           # logger.debugs(sstop_threads)
            if sstop_threads:
                print("thread stopped")
                SolarThread.__track_solar_on = False
                break
            current_time = self.get_time()
            current_altitude = get_altitude(Constants.ST_LATITUDE,Constants.ST_LONGITUDE, current_time, 0)
            difference = current_altitude-last_recorded_altitude
            if difference >= Constants.ST_ANGLE:
                last_recorded_altitude = self.__moveSolar(last_recorded_altitude, current_altitude)
                self.__last_recorded_altitude = last_recorded_altitude
                self.__time_of_last_recorded_altitude = current_time
            else:
                time.sleep(Constants.ST_TIME_LONG)
            print(current_altitude)
            #    logger.debugs(self.__last_recorded_altitude)
            #    logger.debugs(self.__time_of_last_recorded_altitude)
            # ::fle
            #mqtt.publish('altitude', self.__last_recorded_altitude, 2) #<< fle::constant

    def get_time(self):
        time = datetime.now()
        return time.replace(tzinfo=timezone.utc)

    def __moveSolar(self, last_recorded_altitude, current_altitude):
        GPIO.output(relayWest, GPIO.HIGH)
        time.sleep(Constants.ST_TIME_MOVE ) # how long to move rack
        GPIO.output(relayWest, GPIO.LOW)
        time.sleep(Constants.ST_TIME_WAIT_SHORT) # how long to wait after
        return current_altitude

    def get_time_of_last_recorded_altitude(self):
        return self.__time_of_last_recorded_altitude

    def __set_time_of_last_recorded_altitude(self, time):
        self.__time_of_last_recorded_altitude = time
        self.__time_of_last_recorded_altitude = self.__time_of_last_recorded_altitude.replace(tzinfo=timezone.utc) #time thread started
       # logger.debugs("set_start_time called")

    def get_last_recorded__altitude(self):
        return self.__last_recorded_altitude

    def __set_last_recorded__altitude(self, start_time):
        self.__last_recorded_altitude = get_altitude(36.9821103, -121.9722686, start_time, 0)
        self.__time_of_last_recorded_altitude = start_time
        return self.__last_recorded_altitude

'''    def set_angle_to_30_degrees(self):  #how to call under loss of power  go to vertical/go to horizontal?
        super().__set_stop_threads(true)
        current_angle = self.get_time_of_last_recorded_altitude()
        
        if(self.__vertical == true):
            __set_angle_to_30_degrees_from_vertical()
        elif(self.__horizontal == true):
            __set_angle_to_30_degrees_from_horizontal()
        else:
            __set_angle_to_30_from_tracking()

    def set_horizontal(self, bool):
        self.__horizontal = bool
        self.__vertical = not bool

    def set_vertical(self, bool):
        self.__horizontal = bool
        self.__vertical = not bool
'''

def callback():     # channel
    #with app.app_context():
    socketio.emit('alert', {'message' : 'Message from button'})
    #logger.error("emergency shut off")
    GPIO.output(relayWest, GPIO.LOW)
    #global manual, thread
    return


def destroy():
    GPIO.cleanup()
    return


###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

#routes
@app.route('/')
def index():
    """ docstring"""
    print("index called")
    #logger.debugf("app.route('/') BEGIN/END")
    return render_template('index.html')

@socketio.on('relay_on_east')
def relay_on_east():
    """ docstring"""
    #logger.debugs("relay_on_east BEGIN")
    solar_thread.stop_threads()
    #logger.debugs("relay_on_east after bypass")    
    ### ####@@#GPIO    Enable/Disable GPIO
    GPIO.output(relayWest, GPIO.LOW)
    time.sleep(2)
    GPIO.output(relayEast, GPIO.HIGH)
    time.sleep(Constants.CNTRL_SLEEP_TIME)
    GPIO.output(realyEast, GPIO.LOW)
    ####GPIO####      Enable/Disable #@@#GPIO#### ###
    #logger.debugs("relay_on_east END")
    return

@socketio.on('relay_off_east')
def relay_off_east():
    """ docstring"""
    #logger.debugs("relay_off_east BEGIN")
    ### ####@@#GPIO    Enable/Disable GPIO
    GPIO.output(relayEast, GPIO.LOW)
    ####GPIO####      Enable/Disable #@@#GPIO#### ###
    solar_thread.start_threads()
    #logger.debugs("relay_off_east END")
    return

@socketio.on('relay_on_west')
def relay_on_west():
    """ docstring"""
    #logger.debugs("relay_on_west BEGIN")
    solar_thread.stop_threads()
    #logger.debugs("relay_on_west after bypass")    
    ### ####@@#GPIO    Enable/Disable GPIO
    GPIO.output(relayEast, GPIO.LOW)
    time.sleep(2)
    GPIO.output(relayWest, GPIO.HIGH)
    ####GPIO####      Enable/Disable #@@#GPIO#### ###
    #logger.debugs("relay_on_west END")
    return

@socketio.on('realy_off_west')
def relay_off_west():
    """ docstring"""
    #logger.debugs("relay_off_west BEGIN")
    ### ####@@#GPIO    Enable/Disable GPIO
    GPIO.output(relayWest, GPIO.LOW)
    ####GPIO####      Enable/Disable #@@#GPIO#### ###
    solar_thread.start_threads()
    #logger.debugs("relay_off_west END")
    return

@socketio.on('go_to_horizontal')
def go_to_max_angle_horizontal():

    """ docstring"""
    #logger.debugs("go_to_max_angle_horizontal BEGIN")
    solar_thread.stop_threads()
    ### ####@@#GPIO    Enable/Disable GPIO
   # logger.debugs("vertical off")
    GPIO.output(relayWest, GPIO.LOW)
    time.sleep(2)
    #logger.debugs("horizontal on")
    GPIO.output(relayEast, GPIO.HIGH)

    ####GPIO#### Enable/Disable #@@#GPIO#### ###
    logger.debugs("go_to_max_angle_horizontal END")
    return

@socketio.on('go_to_vertical')
def go_to_max_angle_vertical():
    """ docstring"""
    #logger.debugs("go_to_max_angle_vertical BEGIN")
    solar_thread.stop_threads()
    ### ####@@#GPIO    Enable/Disable GPIO
    #logger.debugs("horizontal off")
    GPIO.output(relayEast, GPIO.LOW)
    time.sleep(2)
   # logger.debugs("vertical on")
    GPIO.output(relayWest, GPIO.HIGH)
    ####GPIO####      Enable/Disable #@@#GPIO#### ###
    #logger.debugs("go_to_max_angle_vertical END")
    return

@socketio.on('track')
def start_solar_predicting():
    """
        Start solar predictng
        rack needs to go back to correct angle,then begin thread
    """
   # logger.debugs("start_solar_predicting BEGIN")
    time.sleep(2)
    solar_thread.start_threads()
   # logger.debugs("start_solar_predicting END")
    return

@socketio.on('halt')
def halt_solar_panel():
    """ docstring"""
    #logger.debugs("halt_solar_panel BEGIN")
    ### ####@@#GPIO    Enable/Disable GPIO
    GPIO.output(relayEast, GPIO.LOW)
    GPIO.output(relayWest, GPIO.LOW)
    ####GPIO####      Enable/Disable #@@#GPIO#### ###
    solar_thread.stop_threads()
   # logger.debugs("halt_solar_panel END")
    return


#sockets
# @socketio.on('client_connected')
# def client_connected(json_str):
#     """ docstring"""
#     logger.debugf("socketio.on(client_connected) BEGIN")
#     logger.debugf('received json: %s', json_str)
#     emit('emergency', {'data': 'Connected'})
#     logger.debugf("socketio.on(client_connected) END")

# @socketio.on('publish')
# def handle_publish(json_str):
#     """ docstring"""
#     logger.debugf("socketio.on('publish') BEGIN")
#     data = json.loads(json_str)
#     mqtt.publish(data['topic'], data['message'], data['qos'])
#     logger.debugf("socketio.on('publish') END")

# @socketio.on('subscribe')
# def handle_subscribe(json_str):
#     """ docstring"""
#     logger.debugf("socketio.on(subscribe) BEGIN")
#     data = json.loads(json_str)
#     mqtt.subscribe(data['topic'], data['qos'])
#     logger.debugf("socketio.on(subscribe) END")

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

GPIOdispatch = {
    'relay_on east'                     : relay_on_east,
    'relay_off east'                    : relay_off_east,
    'relay_on west'                     : relay_on_west,
    'relay_off west'                    : relay_off_west,
    'start_solar_predicting predicting' : start_solar_predicting,
    'go_to_max_angle horizontal'        : go_to_max_angle_horizontal,
    'go_to_max_angle vertical'          : go_to_max_angle_vertical,
    'halt_solar_panel halt'             : halt_solar_panel
}

'''def handleAddressCallback(message):
    """ docstring"""
    logger.debugf("handleAddressCallback BEGIN")
    
    jstr = message.payload.decode()

    logger.debugf("Msg=%s=", jstr)

    gpioFunction = GPIOdispatch[jstr]

    logger.debugf("gpioFunction=>%s<=", gpioFunction)

    gpioFunction()

    logger.debugf("handleAddressCallback END")
    return


def on_topic_GpsAddressCallback(client, userdata, message):
    """ docstring"""
    logger.debugf("on_topic_GpsAddressCallback BEGIN")

    handleAddressCallback(message)

    logger.debugf("on_topic_GpsAddressCallback END")
    return


def on_topic_MacAddressCallback(client, userdata, message):
    """ docstring"""
    logger.debugf("on_topic_MacAddressCallback BEGIN")

    handleAddressCallback(message)

    logger.debugf("on_topic_MacAddressCallback END")
    return


def newDhcpTable(message):

    logger.debugf("newDhcpTable BEGIN")

    jstr = message.payload.decode()

    logger.debugf("Msg=%s=", jstr)

    dhclofd = ConfigListOfDict.fromJsonStr(jstr) #start using the new DHCP table

    dhclofd.updateMyCfgDict(hostName, activeNIF, Constants.CFG_VALUE_SYS_TYPE_SLAVE)

    setDhcpConfigLofD(dhclofd)


                    # subscribe to all messages directed to me at my MAc address
    macAddr = activeNIF.getMacAddrAsHexStr()

    mqtt.message_callback_add(macAddr, on_topic_MacAddressCallback)

    mqtt.subscribe(macAddr)


                    # subscribe to all messages directed to me at my GPS address
    #gps = dhclofd.getGps(macAddr, Constants.CFG_VALUE_SYS_TYPE_SLAVE)
    
                    # subscribe to all messages directed to me at my Title
                    # my Title should be the same as my GPS address
    gps = dhclofd.getTitle(macAddr, Constants.CFG_VALUE_SYS_TYPE_SLAVE)

    globalGps.setGps(gps)

    mqtt.message_callback_add(globalGps.getGps(), on_topic_GpsAddressCallback)

    mqtt.subscribe(gps)


    #sendSignonMessageRsp()   fle::send signon rsp to master?????

    logger.debugf("newDhcpTable END")

    return


def makeMessagePayload(ppubTopic, psubTopic):
    """ docstring"""
    logger.debugf("makeMessagePayload BEGIN pub topib %s", ppubTopic)

    myMacAddr = activeNIF.getMacAddrAsHexStr()

    myCfgDct = getDhcpConfigLofD().findConfigDict(myMacAddr, Constants.CFG_VALUE_SYS_TYPE_SLAVE)

    myCfgDct.setMqPub(ppubTopic)

    myCfgDct.setMqSub(psubTopic)

    myCfgDct.setMsgLast()

    jstr = myCfgDct.toJsonStr()

    logger.debugf("makeMessagePayload END")

    return jstr


def sendDhcpReq(psubTopic):
    """ docstring"""
    logger.debugf("sendDhcpReq BEGIN")

    ppubTopic = TopicMaker.makeTopicDhcpReq()

    jstr = makeMessagePayload(ppubTopic, psubTopic)

    logger.debugf("Publishing::topic=%s= msg=%s=", ppubTopic, jstr)

    ret = mqtt.publish(ppubTopic, jstr)

    logger.debugf("Ret::%s", ret)

    logger.debugf("sendDhcpReq END")

    return


def sendSignonRsp(psubTopic):
    """ master sends signon req
        slave responds with signon rsp
    """
    logger.debugf("sendSignonRsp BEGIN")
    
    masterMacAddr = getDhcpConfigLofD().getMacAddrOfMasterForSlave(activeNIF.getMacAddrAsHexStr())

    masterTopicMaker = TopicMaker(masterMacAddr)

    ppubTopic = masterTopicMaker.makeTopicSignonRsp()

    jstr = makeMessagePayload(ppubTopic, psubTopic)

    logger.debugf("Publishing::topic=%s= msg=%s=", ppubTopic, jstr)

    ret = mqtt.publish(ppubTopic, jstr)

    logger.debugf("Ret::%s", ret)

    logger.debugf("sendSignonRsp END")

    return


@mqtt.on_connect() 
def handle_mqtt_connect(client, userdata, flags, rc):
    """
        slave listens
        slave subscribes to all desired topics
    """

    logger.debugf("on_connect BEGIN")

    mqtt.subscribe(slaveTopicMaker.makeTopicDhcpAllReq())
    mqtt.subscribe(slaveTopicMaker.makeTopicDhcpRsp())
    mqtt.subscribe(slaveTopicMaker.makeTopicSignonReq())
    mqtt.subscribe(slaveTopicMaker.makeTopicCmdReq())
    mqtt.subscribe(slaveTopicMaker.makeTopicMisc())

    ##mqtt.subscribe(myMacAddr)

    sendDhcpReq(Constants.CFG_VALUE_DEFAULT_CONNECT)

    logger.debugf("on_connect() END")
    return


@mqtt.on_topic(TopicMaker.makeTopicDhcpAllReq())
def on_topicDhcpAll(client, userdata, message):
    """ master publishes
        slave subscribes to
        slave responds with DHCP Rsp
    """
    on_topic_str = TopicMaker.makeTopicDhcpAllReq()

    logger.debugf("on_topic(%s) BEGIN", on_topic_str)

    newDhcpTable(message)

    sendSignonRsp(on_topic_str)

    logger.debugf("on_topic(%s) END", on_topic_str)
    return


@mqtt.on_topic(slaveTopicMaker.makeTopicDhcpRsp())
def on_topicDhcpRsp(client, userdata, message):
    """ master publishes """
    """ slave subscribes to """
    
    on_topic_str = slaveTopicMaker.makeTopicDhcpRsp()

    logger.debugf("on_topic(%s) BEGIN", on_topic_str)

    newDhcpTable(message)

    sendSignonRsp(on_topic_str)

    logger.debugf("on_topic(%s) END", on_topic_str)

    return


# @mqtt.on_topic(globalGps.getGps())
# def on_topicGps(client, userdata, message):
#     """
#         master publishes
#         slave subscribes to
#     """
#     logger.debugf("on_topic(GPS=%s) BEGIN", globalGps.getGps())

#     sstr = message.payload.decode()
    
#     logger.debugf("msg = %s", sstr)

#     logger.debugf("on_topic(GPS=%s) END", globalGps.getGps())

#     return


""" master publishes """
""" slave subscribes to """

@mqtt.on_topic(slaveTopicMaker.makeTopicCmdReq())
def on_topicCmd(client, userdata, message):
    """
        on_topicCmd
    """
    on_topic_str = slaveTopicMaker.makeTopicCmdReq()

    logger.debugf("on_topic(%s) BEGIN", on_topic_str)

    jstr = message.payload.decode()
    logger.debugf("msg.topic=%s= payload=%s= qos=%s=", message.topic, jstr, message.qos)

    rmtCfg = ConfigDict.fromJsonStr()

    rspTopicMaker = TopicMaker(rmtCfg.getMacAddrSelf())

    rspTopic = rspTopicMaker.makeTopicCmdRsp()

    rmtCfg.setMqPub(rspTopic)

    rmtCfg.setMqSub(on_topic_str)

    rmtCfg.setCmdRsp('Command complete')

    jstr = rmtCfg.toJsonStr()

    mqtt.publish(rspTopic, jstr, qos=0, retain=False)

    logger.debugf("on_topic(%s) END", on_topic_str)

    return


""" master publishes """
""" slave subscribes to """

@mqtt.on_topic(slaveTopicMaker.makeTopicSignonReq())
def on_topicAllSignonReq(client, userdata, message):
    """ docstring"""

    on_topic_str = slaveTopicMaker.makeTopicSignonReq()

    logger.debugf("on_topic(%s) BEGIN", on_topic_str)

    logger.debugf("ID=%s= U=%s= Msg=%s=", client, userdata, message)


    jstr = message.payload.decode()
    logger.debugf("msg.topic=%s= payload=%s= qos=%s=", message.topic, jstr, message.qos)

    rmtCfg = ConfigDict.fromJsonStr(jstr)

    rspTopicMaker = TopicMaker(rmtCfg.getMacAddrSelf())

    myCfgDct = getDhcpConfigLofD().findConfigDict(activeNIF.getMacAddrAsHexStr(), Constants.CFG_VALUE_SYS_TYPE_SLAVE)

    jstr = myCfgDct.toJsonStr()

    mqtt.publish(rspTopicMaker.makeTopicSignonRsp(), jstr, qos=0, retain=False)

    logger.debugf("on_topic(%s) END", on_topic_str)

    return


""" master publishes """
""" slave subscribes to """

@mqtt.on_topic(slaveTopicMaker.makeTopicSignonRsp())
def on_topicSlaveSignOnRsp(client, userdata, message):
    """ docstring"""

    on_topic_str = slaveTopicMaker.makeTopicSignonRsp()

    logger.debugf("on_topic(%s) BEGIN", on_topic_str)

    logger.debugf("ID=%s= U=%s= Msg=%s=", client, userdata, message)

    messagePayloadList = message.payload.decode()

    logger.debugf("msg.topic=%s= payload=%s= qos=%s=", message.topic, messagePayloadList, message.qos)

    #
    # TODO: Do we do anything with the data that the master sends back after signon?
    #

    logger.debugf("on_topic(%s) END", on_topic_str)

    return


@mqtt.on_topic(slaveTopicMaker.makeTopicCmdReq())
def on_topicCmdReq(client, userdata, message):
    """ docstring"""

    on_topic_str = slaveTopicMaker.makeTopicCmdReq()

    logger.debugf("on_topic(%s) BEGIN", on_topic_str)

    jstr = message.payload.decode()

    logger.debugf("msg.topic=%s= payload=%s= qos=%s=", message.topic, jstr, message.qos)

    logger.debugf("on_topic(%s) END", on_topic_str)
    return


@mqtt.on_topic(slaveTopicMaker.makeTopicMisc())
def on_topicMisc(client, userdata, message):
    """ docstring"""

    on_topic_str = slaveTopicMaker.makeTopicMisc()

    logger.debugf("on_topic(%s) BEGIN", on_topic_str)

    #logger.debugf("ID=%s= U=%s= Msg=%s=", client, userdata, message)

    jstr = message.payload.decode()

    logger.debugf("msg.topic=%s= payload=%s= qos=%s=", message.topic, jstr, message.qos)

    logger.debugf("on_topic(%s) END", on_topic_str)

    return



    on_publish
    the publish callback
    This confirms that a specific message was published
        mid:    message ID of the published message 

@mqtt.on_publish()
def handle_mqtt_publish(client, userdata, mid):
    """ docstring"""
    logger.debugf("on_publish() BEGIN")
    logger.debugf('Published message with mid %s', mid)
    logger.debugf("on_publish() END")
    return


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    """
        Capture all messages without a specific handler
        
        TODO::This needs to be rewritten
    """
    print("RECIEVED")
    print("userdata", userdata)
    print("message", message.payload.decode())
    data = dict(
        topic= message.topic,
        payload= message.payload.decode(),
        qos=message.qos,
    )
    messageList = data['payload'].split()
    print("messageList", messageList)
    function = messageList[0].strip()
    messageList.pop(0)
    print("function", function)
    print("messageList length")
    print(len(messageList))
    if len(messageList) > 0:
        data1 =  ' '.join(str(e) for e in messageList)
        print("data", data1)
    else:
        data1 = None
    print("after if statement")
    logger.debugf("************** handle_mqtt_message BEFORE eval **************")
    eval(function)(data1)
    logger.debugf("************** handle_mqtt_message AFTER  eval **************")
    print("socketio.emit")
    mqtt.publish('pushNotification', data1, 2)
    print('push notification called')
    return


@mqtt.on_log()
def handle_mqtt_logging(client, userdata, level, buf):
    """ docstring"""
    #logger.debugf("ID=%s= U=%s= Lvl=%s= buf=%s=", client._client_id, userdata, level, buf)
    logger.debugf("ID=%s= U=%s= Lvl=%s= buf=%s=", client, userdata, level, buf)
    return


@mqtt.on_disconnect()
def handle_mqtt_disconnect():
    """ docstring"""
    logger.debugf('handle_disconnect BEGIN')
    logger.debugf("handle_disconnect END")
    return
'''
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

setup()
if cfgTrackSolarON:
    print("cfgTrackSolarON")
    solar_thread =SolarThread.getInstance()
    solar_thread.start_thread(solar_thread.trackSolar)

### ####@@#GPIO    Enable/Disable GPIO
#GPIO.add_event_detect(button, GPIO.RISING, callback=callback, bouncetime = 1000)
####GPIO####      Enable/Disable #@@#GPIO#### ###

### ####@@#GPIO    Enable/Disable GPIO
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',debug=False)
    #setManual(True)
    destroy()

####GPIO####      Enable/Disable #@@#GPIO#### ###





