from __main__ import socketio
from datetime import datetime as dt, timezone
#import logging
import sys
import threading
import time
from pysolar.solar import get_azimuth
#import pytz
import SysLog
import pytz
#from LogAllOn import LogAllOn
#from LogAllOff import LogAllOff
#from LogF import LogF
#from LogS import LogS
try:
    print("sys.path.append(../common)")
    sys.path.append('../common')
    import Constants
except ImportError:
    print("sys.path.append(/home/pi/raspberry20/common)")
    sys.path.append('/home/pi/raspberry20/common')
    import Constants
from Configuration import ConfigListOfDict

"""
    force commit
"""

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


class ThreadController:
    def __init__(self):
        self.__thread = None
        self.__stop_thread = False

    def start_thread(self, method):
        logger = SysLog.getLogger()
        logger.debugs("start_thread called")
        logger.debugs("self.__thread")
        logger.debugs(self.__thread)
        if self.__thread is None:
            self.__set_stop_thread(False)
            self.__thread = threading.Thread(target=method)
            self.__thread.start()
            print("thread is none")
            return 0
        return -1

    def stop_thread(self):
        logger = SysLog.getLogger()
        logger.debugs("stop thread called")
        self.__set_stop_thread(True)
        self.set_thread(None)

    def get_thread(self):
        return self.__thread

    def set_thread(self, new):
        self.__thread = new

    def get_stop_thread(self):
        return self.__stop_thread

    def __set_stop_thread(self, value):
        self.__stop_thread = value


GPS_COOR_LAT = 0
GPS_COOR_LNG = 1
time_to_wait = .5



class SolarThread(ThreadController):
    __latitude = 37.897542
    __longitude = -121.23825099999999
    __instance = None
    __thread = None
    __last_recorded_azimuth = None
    __macAddr = None
    __current_angle = -45 #pretend calibrate has been called
    __manual_stop_time_angle = None
    __Thread = None
    #__bypass_west = False
    #__bypass_east = False
    __east_relay = False
    __west_relay = False
    __stop_increment_angle = False
    __reset_called = False
    __max_angle_check = False
    @staticmethod
    def getInstance():
        if SolarThread.__instance is None:
            SolarThread.__instance = SolarThread()
        print("This is instance: ", SolarThread.__instance)
        return SolarThread.__instance

    def __init__(self):
        super().__init__()
        logger = SysLog.getLogger()
        logger.debugs("init called")
        if SolarThread.__instance is not None:
            raise Exception("Only one Solar Thread allowed")
#        SolarThread.__rotate_panel_animation(SolarThread.__current_angle)
        return

    @classmethod
    def calibrate_solar_panels(cls):
        SolarThread.__stop_increment_angle = False
        time_to_move = time.time() + 10 #900  CHANGE BACK
        SolarThread.__turn_on_east_relay()
        while time.time() < time_to_move and SolarThread.__stop_increment_angle == False:
            time.sleep(.1)
        SolarThread.stop_all()
        SolarThread.__current_angle = -45

    def setMacAddr(self, macAddr):
        print("SETMACADDR", macAddr)
        logger = SysLog.getLogger()
        logger.debugs("macAddr Solar.py: %s" % macAddr)
        SolarThread.__macAddr = macAddr

    def get_current_angle(cls):
        return SolarThread.__current_angle

    def trackSolar(self):
        logger = SysLog.getLogger()
        myConfigDict = ConfigListOfDict.getInstance().findConfigDict(SolarThread.__macAddr, Constants.CFG_VALUE_SYS_TYPE_SLAVE)
        secsPerDeg = myConfigDict.getTimeToMoveOneDegree()
        print(secsPerDeg)
        gpsCoor = myConfigDict.getGpsCoor()
        gps_lat = gpsCoor[GPS_COOR_LAT]
        gps_lng = gpsCoor[GPS_COOR_LNG]
        last_recorded_azimuth = None
        SolarThread.__stop_increment_angle = False
        if SolarThread.__thread != None:
            print("SolarThread.__thread!=None")
            return -1
        else:
            SolarThread.__thread = self
        #if SolarThread.__current_angle == None: Commented out for testing
        #    print("Please call Calibrate First")
        #    super().stop_thread()

        if SolarThread.__manual_stop_time_angle is not None:
            angle_to_move = SolarThread.__compute_change_in_azimuth()

            if SolarThread.__angle_to_move > 0:
                logger.debugs("Solar Thread turn on west relay")
                SolarThread.increment_panel_angle(angle_to_move, SolarThread.__turn_on_west_relay)

            elif SolarThread.__angle_to_move < 0:
                logger.debugs("Solar Thread turn on east relay")
                SolarThread.increment_panel_angle(angle_to_move, SolarThread.__turn_on_east_relay)
        #Panel should be in correct position from code above
        SolarThread.__manual_stop_time_angle = None

        print("This is SolarThread.__current_angle", SolarThread.__current_angle)
        if last_recorded_azimuth == None:
            last_recorded_azimuth = get_azimuth(SolarThread.__latitude, SolarThread.__longitude, SolarThread.get_time())
        while True:

            logger.debugs("SolarThread")
            if super().get_stop_thread():
                logger.debugs("THREAD STOPPED")
                SolarThread.__thread = None
                break
            current_azimuth = get_azimuth(SolarThread.__latitude, SolarThread.__longitude, SolarThread.get_time())  #gps_lat, gps_lng, current_time, 0)
            print("current azimuth", current_azimuth)
            new_angle = current_azimuth - 180 # change back to 180!!!!
            if new_angle > -45 and new_angle < 45: #when we would start moving the panel
                SolarThread.__reset_called = False # reset...reset for next day
                SolarThread.__max_angle_check = False
                print("This is new angle: ", new_angle)
                print("This is current angle: ", SolarThread.__current_angle)
                difference = new_angle - SolarThread.__current_angle
                print("This is difference: ", difference)
                if difference >= Constants.ST_ANGLE:
                    print("Larger than")
                    self.increment_panel_angle(difference, SolarThread.__turn_on_west_relay)
                elif difference < (-1 * Constants.ST_ANGLE):
                    print("Smaller than")
                    self.increment_panel_angle(difference, SolarThread.__turn_on_east_relay)
                last_recorded_azimuth = current_azimuth
                time.sleep(Constants.ST_TIME_WAIT_SHORT)
            elif 225 < current_azimuth < 280 and SolarThread.__current_angle != 45 and SolarThread.__max_angle_check == False:  #azimuth should be 225 for a 45* angle
                print("notreset")
                difference = 45 - SolarThread.__current_angle + 2
                self.increment_panel_angle(difference, SolarThread.__turn_on_west_relay)
                SolarThread.__max_angle_check = true
            elif ((0 < current_azimuth and current_azimuth < 90) or current_azimuth >= 280) and SolarThread.__reset_called == False:
                print("reset")
                difference = -100
                self.increment_panel_angle(difference, SolarThread.__turn_on_east_relay)
                SolarThread.__reset_called = True
            else:
                time.sleep(Constants.ST_TIME_WAIT_SHORT)
                logger.debugs("new angle %s" %new_angle)
                logger.debugs("current angle %s" %SolarThread.__current_angle)

    def increment_panel_angle(self, angle_to_move, direction):  #direction is a passed method
        secsPerDeg = ConfigListOfDict.getInstance().findConfigDict(SolarThread.__macAddr, Constants.CFG_VALUE_SYS_TYPE_SLAVE).getTimeToMoveOneDegree()
        print("SolarThread.__stop_increment: ", SolarThread.__stop_increment_angle)
        print("angle to move: ", angle_to_move)
        SolarThread.__stop_increment_angle = False
        if angle_to_move + SolarThread.__current_angle > 45:
            print( ">45")
            angle_to_move = 45 - SolarThread.__current_angle   # +1 for good luck  find reasonable time to reach max angle
            time_to_move = time.time() + (abs(angle_to_move) *  10) + 20
        elif angle_to_move + SolarThread.__current_angle < -45:
            print( "<45")
            angle_to_move = -45 - SolarThread.__current_angle  # +1 for good luck  find reasonable time to reach max angle
            time_to_move = time.time() + (abs(angle_to_move) *  10) + 20 
        else:
            print("not either case")
            time_to_move = time.time() + (abs(angle_to_move) *  10)
        print("time to move :", time_to_move - time.time())
        sign = direction()
        while(time.time() <= time_to_move + 1 and SolarThread.__stop_increment_angle != True):
            print("__stop_increment_angle: ", SolarThread.__stop_increment_angle)
            SolarThread.__current_angle = SolarThread.__current_angle + (sign*(1/(2 * 10)))
            SolarThread.__update_solar_animation()
            if SolarThread.__current_angle > 45:
                SolarThread.__current_angle = 45
                SolarThread.__update_solar_animation()
            elif SolarThread.__current_angle < -45:
                SolarThread.__current_angle = -45
                SolarThread.__update_solar_animation()
            time.sleep(.5) #constant
            print(SolarThread.__current_angle)
        
        SolarThread.stop_all()
        SolarThread.__stop_increment_angle = False

    @classmethod
    def __update_solar_animation(cls):
        socketio.emit('rotate_panel_animation_js', SolarThread.__current_angle)


    @classmethod
    def get_time(cls):
        dtime = dt.now(pytz.timezone("America/Los_Angeles"))
        print(dtime)
        return dtime #dtime.replace(tzinfo=timezone.America/Los_Angeles)

    def turn_on_west_relay_manual(self):
        logger = SysLog.getLogger()
        SolarThread.__stop_increment_angle = False
        print(SolarThread.__current_angle)
        print("SolarThread.__west_relay: ", SolarThread.__west_relay)
        while SolarThread.__stop_increment_angle == False:
            if SolarThread.__west_relay == False:
                SolarThread.__turn_on_west_relay()
                SolarThread.__west_relay = True
            SolarThread.__current_angle = SolarThread.__current_angle + 1/100 # make constant
            SolarThread.__update_solar_animation()
            print("SolarThread_current_angle: ", SolarThread.__current_angle)
            time.sleep(.1)
        SolarThread.turn_off_relays()
        SolarThread.__west_relay = False
        SolarThread.__stop_increment_angle = False

    def turn_on_east_relay_manual(self):
        logger = SysLog.getLogger()
        SolarThread.__stop_increment_angle = False
        print(SolarThread.__current_angle)
        print("SolarThread.__east_relay: ", SolarThread.__east_relay)
        while SolarThread.__stop_increment_angle == False:
            if SolarThread.__east_relay == False:
                SolarThread.__turn_on_east_relay()
                SolarThread.__east_relay = True
            if SolarThread.__current_angle > -45: # make constant
                SolarThread.__current_angle = SolarThread.__current_angle - 1/100 #make constant
                SolarThread.__update_solar_animation()
            print("SolarThread_current_angle: ", SolarThread.__current_angle)
            time.sleep(.1)
        SolarThread.turn_off_relays()
        SolarThread.__east_relay = False
        SolarThread.__stop_increment_angle = False


    def go_to_vertical_manual(self):  # <<< fle::no parameter::class method?
        logger = SysLog.getLogger()
        SolarThread.__stop_increment_angle = False
        secsPerDeg = 10 #ConfigListOfDict.getInstance().findConfigDict(self.__macAddr, Constants.CFG_VALUE_SYS_TYPE_SLAVE).getTimeToMoveOneDegree()
        difference = 45 - SolarThread.__current_angle + .5
        self.increment_panel_angle(difference, SolarThread.__turn_on_west_relay)

    def go_to_horizontal_manual(self):
        logger = SysLog.getLogger()
        SolarThread.__stop_increment_angle = False
        secsPerDeg = 10
        difference = -45 - SolarThread.__current_angle -.5  # make -2 constant, to make sure device is at -45
        print("this is difference: ", difference)
        print("SolarThread.__turn on east relay", SolarThread.__turn_on_east_relay)
        self.increment_panel_angle(difference, SolarThread.__turn_on_east_relay)

    def move_to_22_degrees(self):
        SolarThread.__stop_increment_angle = False
        secsPerDeg = 10
        difference = -22 - SolarThread.__current_angle
        if difference > 0:
            self.increment_panel_angle(difference, SolarThread.__turn_on_west_relay)
        elif difference < 0:
            self.increment_panel_angle(difference, SolarThread.__turn_on_east_relay)

    @classmethod
    def set_stop_increment_angle(cls, bool):
        SolarThread.__stop_increment_angle = bool
    
    @classmethod
    def __turn_on_west_relay(cls):
        ### #@GPIO@#      Enable/Disable GPIO
        GPIO.output(Constants.RELAY_EAST, GPIO.LOW)
        ##@GPIO@##        Enable/Disable #@GPIO@# ###
        time.sleep(time_to_wait)
        ### #@GPIO@#      Enable/Disable GPIO
        GPIO.output(Constants.RELAY_WEST, GPIO.HIGH)
        ##@GPIO@##        Enable/Disable #@GPIO@# ###
        return 1

    @classmethod
    def __turn_on_east_relay(self):
        ### #@GPIO@#      Enable/Disable GPIO
        GPIO.output(Constants.RELAY_WEST, GPIO.LOW)
        ##@GPIO@##        Enable/Disable #@GPIO@# ###
        time.sleep(time_to_wait)
        ### #@GPIO@#      Enable/Disable GPIO
        GPIO.output(Constants.RELAY_EAST, GPIO.HIGH)
        ##@GPIO@##        Enable/Disable #@GPIO@# ###
        return -1

    @classmethod
    def stop_all(cls):
        time.sleep(time_to_wait) 
        SolarThread.__stop_increment_angle = True
        SolarThread.__east_relay = False
        SolarThread.__west_relay =False
        SolarThread.turn_off_relays()
        SolarThread.__max_angle_check = False
        SolarThread.__reset_called = False
    @classmethod 
    def turn_off_relays(cls):
        ### #@GPIO@#      Enable/Disable GPIO
        print("turn_off_relays")
        GPIO.output(Constants.RELAY_WEST, GPIO.LOW)
        GPIO.output(Constants.RELAY_EAST, GPIO.LOW)
        ##@GPIO@##        Enable/Disable #@GPIO@# ###
        return

    @classmethod
    def __time_in_seconds(cls, t):
        return  t.timestamp()



