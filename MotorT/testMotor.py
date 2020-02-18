""" sFlask/main.py Slave Raspberry Pi """


#import json
#import logging
import sys
import threading
import time
from datetime import datetime as dt
from datetime import timezone
#import uuid
from gevent import monkey
monkey.patch_all()
from pysolar.solar import *
import pytz 
from flask import Flask, render_template  # , request
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
#from flask_googlemaps import GoogleMaps, Map, icons
#from flask_mqtt import Mqtt
from flask_socketio import SocketIO, emit   #, send
import RPi.GPIO as GPIO

try:
    print("sys.path.append(../common)")
    sys.path.append('../common')
    import Constants
except ImportError:
    print("sys.path.append(/home/pi/raspberry20/common)")
    sys.path.append('/home/pi/raspberry20/common')
    import Constants




cfgTrackSolarON = True

app = Flask(__name__)

app.debug = True
app.env = 'development'
app.secret_key = 'development key'


relayWest = 23
relayEast = 22



Bootstrap(app)
#mqtt = MyMqtt(app)
socketio = SocketIO(app, async_mode='gevent')


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



class ThreadController:
    def __init__(self):
        self.__thread = None
        self.__stop_thread = False

    def start_thread(self, method):
        print("start_thread called")
        print("self.__thread")
        print(self.__thread)
        if self.__thread is None:
            self.__set_stop_thread(False)
            self.__thread = threading.Thread(target=method)
            self.__thread.start()
            return 0
        return -1

    def stop_thread(self):
        print("stop thread called")
       # logger.debugs("Stop thread called")
        self.__set_stop_thread(True)
       # self.set_thread(None)

    def get_thread(self):
        return self.__thread

    def __set_thread(self, new):
        self.__thread = new

    def get_stop_thread(self):
        return self.__stop_thread

    def __set_stop_thread(self, value):
        self.__stop_thread = value


class SolarThread(ThreadController):
    __instance = None

    @staticmethod
    def getInstance():
        if SolarThread.__instance is None:    # fle::
            SolarThread.__instance = SolarThread()
        return SolarThread.__instance

    def __init__(self):
        print("init called")
        if SolarThread.__instance !=  None:
            raise Exception("Only one Solar Thread allowed")

        super().__init__()
        #SolarThread.__instance = self       # fle::
        self.__last_recorded_altitude = None
        self.__time_of_last_recorded_altitude = None
        self.__time_thread_started = None
        self.__vertical = None
        self.__horizontal = None
        self.__track_solar_on = False

    def trackSolar(self):
        if self.__track_solar_on:
            return -1

        self.__track_solar_on = True
        start_time = self.get_time() #time thread started
        last_recorded_altitude = self.__set_last_recorded__altitude(start_time)
        self.__set_time_of_last_recorded_altitude(start_time)
        while True:
            print("trackSolar")
            sstop_threads = super().get_stop_thread()
            print("this is sstop threads")
            print(sstop_threads)
           # logger.debugs("this is stop_threads")
           # logger.debugs(sstop_threads)
            if sstop_threads:
                print("thread stopped")
                self.__track_solar_on = False
                super()._ThreadController__set_thread(None)
                break
            current_time = self.get_time()
            current_altitude = get_altitude(Constants.ST_LATITUDE,Constants.ST_LONGITUDE, current_time, 0)
            difference = current_altitude-last_recorded_altitude
            if difference >= Constants.ST_ANGLE:
                last_recorded_altitude = SolarThread.__moveSolar(current_altitude)
                self.__last_recorded_altitude = last_recorded_altitude
                self.__time_of_last_recorded_altitude = current_time
            else:
                time.sleep(Constants.ST_TIME_LONG)
            print(current_altitude)
            #    logger.debugs(self.__last_recorded_altitude)
            #    logger.debugs(self.__time_of_last_recorded_altitude)
            # ::fle
            #mqtt.publish('altitude', self.__last_recorded_altitude, 2) #<< fle::constant

    @staticmethod
    def get_time():
        dtime = dt.now()
        return dtime.replace(tzinfo=timezone.utc)

    @staticmethod
    def __moveSolar(current_altitude):
        print("moveSolar")
        GPIO.output(relayWest, GPIO.HIGH)
        time.sleep(Constants.ST_TIME_MOVE ) # how long to move rack
        GPIO.output(relayWest, GPIO.LOW)
        time.sleep(Constants.ST_TIME_WAIT_SHORT) # how long to wait after
        return current_altitude

    def get_time_of_last_recorded_altitude(self):
        return self.__time_of_last_recorded_altitude

    def __set_time_of_last_recorded_altitude(self, ttime):
        self.__time_of_last_recorded_altitude = ttime
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
    GPIO.output(relayEast, GPIO.LOW)
    GPIO.output(relayWest, GPIO.LOW)
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

@socketio.on('east_for_duration')
def east_for_duration():
    """ docstring"""
    solar_thread.stop_thread()
    GPIO.output(relayWest, GPIO.LOW)
    time.sleep(Constants.RELAY_CHANGE_DELAY)
    for x in range(Constants.RELAY_NUM_OF_TIMES):
        print(x)
        GPIO.output(relayWest, GPIO.LOW)
        GPIO.output(relayEast, GPIO.HIGH)
        time.sleep(Constants.RELAY_CNTRL_SLEEP_TIME)
        GPIO.output(relayEast, GPIO.LOW)
        time.sleep(Constants.RELAY_CNTRL_SLEEP_TIME)
    return



@socketio.on('west_for_duration')
def west_for_duration():
    """ docstring"""
    solar_thread.stop_thread()
    GPIO.output(relayEast, GPIO.LOW)
    time.sleep(Constants.RELAY_CHANGE_DELAY)
    for x in range(Constants.RELAY_NUM_OF_TIMES):
        print(x)
        GPIO.output(relayEast, GPIO.LOW)
        GPIO.output(relayWest, GPIO.HIGH)
        time.sleep(Constants.RELAY_CNTRL_SLEEP_TIME)
        GPIO.output(relayWest, GPIO.LOW)
        time.sleep(Constants.RELAY_CNTRL_SLEEP_TIME)
    return




@socketio.on('relay_on_east')
def relay_on_east():
    """ docstring"""
    #logger.debugs("relay_on_east BEGIN")
    solar_thread.stop_thread()
    #logger.debugs("relay_on_east after bypass")    
    ### ####@@#GPIO    Enable/Disable GPIO
    GPIO.output(relayWest, GPIO.LOW)
    time.sleep(Constants.RELAY_CHANGE_DELAY)
    GPIO.output(relayEast, GPIO.HIGH)
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
    #logger.debugs("relay_off_east END")
    return

@socketio.on('relay_on_west')
def relay_on_west():
    """ docstring"""
    #logger.debugs("relay_on_west BEGIN")
    solar_thread.stop_thread()
    #logger.debugs("relay_on_west after bypass")    
    ### ####@@#GPIO    Enable/Disable GPIO
    GPIO.output(relayEast, GPIO.LOW)
    time.sleep(Constants.RELAY_CHANGE_DELAY)
    GPIO.output(relayWest, GPIO.HIGH)
    ####GPIO####      Enable/Disable #@@#GPIO#### ###
    #logger.debugs("relay_on_west END")
    return

@socketio.on('relay_off_west')
def relay_off_west():
    """ docstring"""
    #logger.debugs("relay_off_west BEGIN")
    ### ####@@#GPIO    Enable/Disable GPIO
    GPIO.output(relayWest, GPIO.LOW)
    ####GPIO####      Enable/Disable #@@#GPIO#### ###
    #logger.debugs("relay_off_west END")
    return

@socketio.on('go_to_horizontal')
def go_to_max_angle_horizontal():

    """ docstring"""
    print("horizontal")
    #logger.debugs("go_to_max_angle_horizontal BEGIN")
    solar_thread.stop_thread()
    ### ####@@#GPIO    Enable/Disable GPIO
   # logger.debugs("vertical off")
    GPIO.output(relayWest, GPIO.LOW)
    time.sleep(Constants.RELAY_CHANGE_DELAY)
    #logger.debugs("horizontal on")
    GPIO.output(relayEast, GPIO.HIGH)
    time.sleep(Constants.RELAY_CNTRL_MAX_ANGLE_TIME_HORIZONTAL)
    GPIO.output(relayEast, GPIO.LOW)

    ####GPIO#### Enable/Disable #@@#GPIO#### ###
    #logger.debugs("go_to_max_angle_horizontal END")
    return

@socketio.on('go_to_vertical')
def go_to_max_angle_vertical():
    """ docstring"""
    print("vertical")
    #logger.debugs("go_to_max_angle_vertical BEGIN")
    solar_thread.stop_thread()
    ### ####@@#GPIO    Enable/Disable GPIO
    #logger.debugs("horizontal off")
    GPIO.output(relayEast, GPIO.LOW)
    time.sleep(Constants.RELAY_CHANGE_DELAY)
   # logger.debugs("vertical on")
    GPIO.output(relayWest, GPIO.HIGH)
#    time.sleep(Constants.RELAY_CNTRL_MAX_ANGLE_TIME_VERTICAL)
 #   GPIO.output(relayWest, GPIO.LOW)
    ####GPIO####      Enable/Disable #@@#GPIO#### ###
    #logger.debugs("go_to_max_angle_vertical END")
    return

@socketio.on('track')
def start_solar_predicting():
    """
        Start solar predictng
        rack needs to go back to correct angle,then begin thread
    """
    print("track")
   # logger.debugs("start_solar_predicting BEGIN")
    time.sleep(Constants.RELAY_CHANGE_DELAY)
    solar_thread.start_thread(solar_thread.trackSolar)
   # logger.debugs("start_solar_predicting END")
    return

@socketio.on('halt')
def halt_solar_panel():
    """ docstring"""
    print("halt")
    #logger.debugs("halt_solar_panel BEGIN")
    ### ####@@#GPIO    Enable/Disable GPIO
    GPIO.output(relayEast, GPIO.LOW)
    GPIO.output(relayWest, GPIO.LOW)
    ####GPIO####      Enable/Disable #@@#GPIO#### ###
    solar_thread.stop_thread()
   # logger.debugs("halt_solar_panel END")
    return


global loop
loop = True
@socketio.on('loop')
def loop():
    print("loop")
    global loop
    loop = True
    SolarThread.getInstance().stop_thread() #
    while(loop):
        GPIO.output(Constants.RELAY_EAST, GPIO.LOW)
        time.sleep(Constants.RELAY_CHANGE_DELAY)
        GPIO.output(Constants.RELAY_WEST, GPIO.HIGH)
        time.sleep(Constants.RELAY_CNTRL_SLEEP_TIME)
        GPIO.output(Constants.RELAY_WEST, GPIO.LOW)
        time.sleep(Constants.RELAY_CHANGE_DELAY)
        GPIO.output(Constants.RELAY_EAST, GPIO.HIGH)
        time.sleep(Constants.RELAY_CNTRL_SLEEP_TIME)
        
    return


@socketio.on('halt_solar_loop')
def halt_stop_loop():
    print("halt_stop_loop")
    global loop
    loop = False
    GPIO.output(Constants.RELAY_WEST, GPIO.LOW)
    GPIO.output(Constants.RELAY_EAST, GPIO.LOW)
    return




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


setup()
if cfgTrackSolarON:
    print("cfgTrackSolarON")
    solar_thread =SolarThread.getInstance()
    solar_thread.start_thread(solar_thread.trackSolar)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',debug=False)
    #setManual(True)
    destroy()
####GPIO####      Enable/Disable #@@#GPIO#### ###
