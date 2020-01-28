
""" sFlask/main.py Slave Raspberry Pi """

#from gevent import monkey		## ****** WHERE DOES THIS GO???? ******
#monkey.patch_all()				## ****** WHERE DOES THIS GO???? ******
import os
import logging
import sys
import time
from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template  # , request
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from flask_socketio import SocketIO #, emit, send
try:
    print("sys.path.append(../common)")
    sys.path.append('../common')
    import Constants
except ImportError:
    print("sys.path.append(/home/pi/raspberry30/common)")
    sys.path.append('/home/pi/raspberry30/common')
    import Constants
from ActiveNIF import ActiveNIF
#import Configuration
from Configuration import ConfigDict, ConfigListOfDict
import SysLog
from HostName import HostName
from LogAllOn import LogAllOn
#from LogAllOff import LogAllOff
#from LogF import LogF
#from LogS import LogS
from MyMqtt import MyMqtt
from TopicMaker import TopicMaker
from Utilities import *

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
#               """ #@GPIO@#   Enable/Disable GPIO            <<<< Disable GPIO
#       to
#               ### #@GPIO@#   Enable/Disable GPIO            <<<< Enable GPIO
#
# End of Code Block
#
#       Change 
#               #@GPIO@# """                                <<<< Disable GPIO
#       to
#               #@GPIO@# ###                                <<<< Enable GPIO
#

### #@GPIO@#    Enable/Disable GPIO
import RPi.GPIO as GPIO
##@GPIO@##        Enable/Disable #@GPIO@# ###

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
ConfigListOfDict.getInstance()
def initSysLog(fname):
    """ docstring """
    syslog = SysLog.initialize(__name__, fname, "%(asctime)s - %(name)s - %(levelname)s - %(message)s", logging.DEBUG)
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

LOG_FNAME = 'slave.log'

logger = initSysLog(LOG_FNAME)

logger.info("Log Started")

cfgTrackSolarON = True
#cfgTrackSolarON = False

signonThread = None

mySysType = Constants.CFG_VALUE_SYS_TYPE_SLAVE

activeNIF = ActiveNIF()

hostName = HostName()

slaveTopicMaker = TopicMaker(activeNIF.getMacAddrAsHexStr())

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

initConfig(Constants.CFG_FILE_PATH, Constants.CFG_FILE_NAME_STARTUP)

ConfigListOfDict.getInstance().updateMyCfgDict(hostName, activeNIF, mySysType)

def debugWriteConfigFileUpd(fname):
    debugWriteConfigFile(Constants.CFG_FILE_PATH, fname + '.upd')
    return

debugWriteConfigFileUpd(Constants.CFG_FILE_NAME_DEBUG_SLAVE)

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

app = Flask(__name__)

app.debug = True
app.env = 'development'
app.secret_key = 'development key'

toolbar = DebugToolbarExtension(app)

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = ConfigListOfDict.getInstance().getIpAddrBroker()
app.config['MQTT_BROKER_PORT'] = ConfigListOfDict.getInstance().getPortBroker(activeNIF.getMacAddrAsHexStr(), Constants.CFG_VALUE_SYS_TYPE_SLAVE)
app.config['MQTT_CLIENT_ID'] = ''
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 120
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_LAST_WILL_TOPIC'] = 'home/lastwill'
app.config['MQTT_LAST_WILL_MESSAGE'] = activeNIF.getMacAddrAsHexStr() +' disconnect'
app.config['MQTT_LAST_WILL_QOS'] = 2

Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
mqtt = MyMqtt(app)
socketio = SocketIO(app, async_mode='gevent')
from Solar import SolarThread   #  ThreadController,
#from Solar import #animationThread
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

class MyGps():

    def __init__(self):
        self._gpsStr = None
        return

    def getGps(self):
        return self._gpsStr

    def setGps(self, gpsStr):
        self._gpsStr = gpsStr
        return

globalGps = MyGps()

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

def callback():
    #with app.app_context():
    socketio.emit('alert', {'message' : 'Message from button'})
    logger.error("emergency shut off")
    ### #@GPIO@#     Enable/Disable GPIO
    GPIO.output(Constants.RELAY_WEST, GPIO.LOW)
    ##@GPIO@##         Enable/Disable #@GPIO@# ###
    #global manual, thread
    return

def destroy():
    ### #@GPIO@#     Enable/Disable GPIO
    GPIO.cleanup()
    ##@GPIO@##         Enable/Disable #@GPIO@# ###
    return

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################"
global current_task, BUTTONS_ENABLED, BUTTONS_DISABLED, button_state
current_task = "None"
BUTTONS_ENABLED = "enablebuttons"
BUTTONS_DISABLED = "disablebuttons"
button_state = "enablebuttons"

def update_current_task(value):
    global current_task
    current_task = value

def get_current_task():
    global current_task
    return current_task

def update_button_state(value):
    global button_state
    button_state = value

def get_button_state():
    global button_state
    return button_state

def setup():
    """ docstring"""
    #logger.debugs("Setup BEGIN")
    ### #@GPIO@#     Enable/Disable GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    #GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(Constants.RELAY_WEST, GPIO.OUT)
    GPIO.setup(Constants.RELAY_EAST, GPIO.OUT)
    ##@GPIO@##         Enable/Disable #@GPIO@# ###
    SolarThread.turn_off_relays() 
    #logger.debugs("Setup END")
    return


#routes
@app.route('/')
def index():
    """ docstring"""
    logger.debugf("index called::app.route('/') BEGIN/END")
    print("SUP")
    currentAngleOfPanel = SolarThread.getInstance().get_current_angle()
    print("currentAngleOfPanel", currentAngleOfPanel)
    currentTask = get_current_task()
    button_state = get_button_state()
    return render_template('index.html', currentAngleOfPanel = currentAngleOfPanel, currentTask = currentTask, button_state = button_state )

@socketio.on('relay_on_east')
def relay_on_east():
    """ docstring"""
    logger.debugs("relay_on_east BEGIN")
    SolarThread.getInstance().stop_thread() #
    #animationThread.getInstance().stop_thread()
    socketio.emit("update_alert", "Held East")
    update_current_task("Held East")
    update_button_state(BUTTONS_DISABLED)
    SolarThread.getInstance().turn_on_east_relay_manual()
    logger.debugs("relay_on_east END")
    return

@socketio.on('relay_on_west')
def relay_on_west():
    """ docstring"""
    logger.debugs("relay_on_west BEGIN")
    SolarThread.getInstance().stop_thread()
    socketio.emit("update_alert", "Held West")
    update_current_task("Held West")
    update_button_state(BUTTONS_DISABLED)
    SolarThread.getInstance().turn_on_west_relay_manual()
    logger.debugs("relay_on_west END")
    return

@socketio.on('go_to_morning_position')
def go_to_morning_position():
    """ docstring"""
    logger.debugs("go_to_max_angle_horizontal BEGIN")
    SolarThread.getInstance().stop_thread() #
    #animationThread.getInstance().stop_thread()
    logger.debugs("vertical off")
    logger.debugs("horizontal on")
    socketio.emit("disableButtons", broadcast = True)
    socketio.emit("update_alert", "Morning Position")
    update_button_state(BUTTONS_DISABLED)
    update_current_task("Morning Position")
    SolarThread.getInstance().go_to_morning_position_manual()
 #   SolarThread.getInstance().turn_on_east_relay_manual()
 #   time.sleep(Constants.RELAY_CNTRL_MAX_ANGLE_TIME_HORIZONTAL)
 #   SolarThread.turn_off_east_relay_manual()
    logger.debugs("go_to_max_angle_horizontal END")
    socketio.emit("update_alert","Morning Position stopped")
    update_current_task("Morning Position stopped")
    return

@socketio.on('go_to_evening_position')
def go_to_evening_position():
    """ docstring"""
    logger.debugs("go_to_max_angle_vertical BEGIN")
    SolarThread.getInstance().stop_thread() #
    logger.debugs("horizontal off")
    logger.debugs("vertical on")
    socketio.emit("disableButtons", broadcast = True)
    update_button_state(BUTTONS_DISABLED)
    socketio.emit("update_alert", "Evening Position")
    update_current_task("Evening Position")
    SolarThread.getInstance().go_to_evening_position_manual()
    socketio.emit("update_alert","Evening Position stopped")
    update_current_task("Evening Position stopped")
    return

@socketio.on('calibrate')
def calibrate():
    print('calibrate')
    SolarThread.getInstance().stop_thread()
    SolarThread.getInstance().stop_all()
    socketio.emit("disableButtons", broadcast = True)
    socketio.emit("update_alert", "Calibrate")
    update_button_state(BUTTONS_DISABLED)
    update_current_task("Calibrate")
    SolarThread.getInstance().calibrate_solar_panel()
    socketio.emit("update_alert","Calibrate stopped")
    update_current_task("Calibrate stopped")
    #animationThread.getInstance().start_thread(#animationThread.getInstance().calibrate_animation)

@socketio.on('move_to_22_degrees')
def move_to_22_degrees():
    print('move_to_22_degrees')
    SolarThread.getInstance().stop_thread()
    SolarThread.getInstance().stop_all()
    socketio.emit("disableButtons", broadcast = True)
    socketio.emit("update_alert", "22 Degrees")
    update_button_state(BUTTONS_DISABLED)
    update_current_task("22 Degrees")
    SolarThread.getInstance().move_to_22_degrees()
    socketio.emit("update_alert","22 Degrees Stopped")
    update_current_task("22 Degrees stopped")

@socketio.on('track')
def start_solar_predicting():
    print("track")
    SolarThread.getInstance().stop_thread()
    SolarThread.getInstance().stop_all()
    socketio.emit("disableButtons", broadcast = True)
    socketio.emit("update_alert", "Tracking Sun")
    update_current_task("Track Solar")
    update_button_state(BUTTONS_DISABLED)
    SolarThread.getInstance().start_thread(SolarThread.getInstance().trackSolar) #
    logger.debugs("start_solar_predicting END")
    return

@socketio.on('halt')
def halt_solar_panel():
    """ docstring"""
    logger.debugs("halt_solar_panel BEGIN")
    socketio.emit("update_alert", "Halt")
    socketio.emit("enableButtons", broadcast = True)
    update_current_task("Halt")
    update_button_state(BUTTONS_ENABLED)
    SolarThread.getInstance().set_stop_increment_angle(True)
    SolarThread.getInstance().stop_all()
    logger.debugs("halt_solar_panel END")
    return

@socketio.on('shut_off')
def shut_off():
    socketio.emit("update_alert", "Shut Down")
    update_current_task("Shut Down")
    update_button_state(BUTTONS_DISABLED)
    time.sleep(2)
    os.system("sudo shutdown now")

#    socketio.emit('enableButtons')
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

GPIOdispatch = {
    'relay_on east'                     : relay_on_east,
    'relay_on west'                     : relay_on_west,
    'start_solar_predicting track' : start_solar_predicting,
    'go_to_morning_position' : go_to_morning_position,
    'go_to_evening_position'   : go_to_evening_position,
    'halt_solar_panel halt'             : halt_solar_panel
}

def handleAddressCallback(message):
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

    ConfigListOfDict.fromJsonStr(jstr) #start using the new DHCP table

    ConfigListOfDict.getInstance().updateMyCfgDict(hostName, activeNIF, mySysType)

    debugWriteConfigFileUpd(Constants.CFG_FILE_NAME_DEBUG_SLAVE)

                    # subscribe to all messages directed to me at my MAc address
    mmacAddr = activeNIF.getMacAddrAsHexStr()

    mqtt.message_callback_add(mmacAddr, on_topic_MacAddressCallback)

    mqtt.subscribe(mmacAddr)

                    # subscribe to all messages directed to me at my Title
                    # my Title should be the same as my GPS address
    gps = ConfigListOfDict.getInstance().getTitle(mmacAddr, mySysType)

    globalGps.setGps(gps)

    mqtt.message_callback_add(globalGps.getGps(), on_topic_GpsAddressCallback)

    mqtt.subscribe(gps)

    logger.debugf("newDhcpTable END")

    return


def makeMessagePayload(ppubTopic, psubTopic):
    """ docstring"""
    logger.debugf("makeMessagePayload BEGIN pub topib %s", ppubTopic)

    myMacAddr = activeNIF.getMacAddrAsHexStr()

    myCfgDct = ConfigListOfDict.getInstance().findConfigDict(myMacAddr, mySysType)

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
    
    masterMacAddr = ConfigListOfDict.getInstance().getMacAddrOfMasterForSlave(activeNIF.getMacAddrAsHexStr())

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

    myCfgDct = ConfigListOfDict.getInstance().findConfigDict(activeNIF.getMacAddrAsHexStr(), mySysType)

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


"""
    on_publish
    the publish callback
    This confirms that a specific message was published
        mid:    message ID of the published message 
"""
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


if __name__ == '__main__':
    setup()

    macAddr = activeNIF.getMacAddrAsHexStr()
    logger.debugs("macAddress slave.py: %s" % macAddr)
    cfgDct = ConfigListOfDict.getInstance().findConfigDict(macAddr, Constants.CFG_VALUE_SYS_TYPE_SLAVE)
    
    if cfgTrackSolarON:
        logger.debugs("cfgTrackSolarON")
        SolarThread.getInstance()
        SolarThread.getInstance().setMacAddr(macAddr)
        SolarThread.getInstance().set_latitude()
        SolarThread.getInstance().set_longitude()
        SolarThread.getInstance().set_secs_per_deg()
        SolarThread.getInstance().set_sleep()
        SolarThread.getInstance().set_increment_angle()
        SolarThread.getInstance().set_track_angle_west()
        SolarThread.getInstance().set_track_angle_east()
        SolarThread.getInstance().set_azimuth_angle_start()
        SolarThread.getInstance().set_azimuth_angle_stop()
        #animationThread.getInstance().setMacAddr(macAddr)
        logger.debugs("after setMacAddr slave.py")
#        SolarThread.getInstance().start_thread(SolarThread.getInstance().findPositionOnStart)  #
#        SolarThread.getInstance().start_thread(SolarThread.getInstance().trackSolar)
        ##animationThread.getInstance().start_thread(#animationThread.getInstance().findPositionOnStart())
    # host=ip Addr or host name to listen on

    listenIpAddr = activeNIF.getIpAddr()

    httpPort = cfgDct.getPortHttp()
    
    logger.infof("%s, %s, at MAC addr %s, listening on Host/IP %s port %s",
                 hostName.get(), mySysType, macAddr, listenIpAddr, httpPort)
    #
    # run method, debug parameter
    #
    # If true, python will automatically reload the program when it detects a change
    # in a source file.  When testing and debuging, this is quite convenient; however,
    # it causes the program to run twice at startup
    #
    socketio.run(app, host='192.168.0.101', port = 5000,debug = False) #host=listenIpAddr, port=httpPort, debug=False)

    destroy()
