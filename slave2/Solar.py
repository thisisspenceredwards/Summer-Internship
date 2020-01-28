from datetime import datetime as dt #, timezone
#import logging
#from flask_socketio import SocketIO
import sys
import threading
import time
from pysolar.solar import get_azimuth
import pytz
import SysLog
from __main__ import socketio
#from Slave import socketio #fle
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
            self.set_stop_thread(False)
            self.__thread = threading.Thread(target=method)
            self.__thread.start()
            print("thread was none")
            return 0
        return -1

    def stop_thread(self):
        logger = SysLog.getLogger()
        logger.debugs("stop thread called")
        self.set_stop_thread(True)

    def get_thread(self):
        return self.__thread

    def set_thread(self, new):
        self.__thread = new

    def get_stop_thread(self):
        return self.__stop_thread

    def set_stop_thread(self, value):
        self.__stop_thread = value


class SolarThread(ThreadController):
    
    __instance = None

    @staticmethod
    def getInstance():
        if SolarThread.__instance is None:
            SolarThread.__instance = SolarThread()
        print("This is instance: ", SolarThread.__instance)
        return SolarThread.__instance

    def __get_dictionary(self):
        return ConfigListOfDict.getInstance().findConfigDict(self.__macAddr, Constants.CFG_VALUE_SYS_TYPE_SLAVE)

    def set_latitude(self):
        self.__latitude = self.__get_dictionary().getLatitude()
    
    def set_longitude(self):
        self.__longitude = self.__get_dictionary().getLongitude()

    def set_sleep(self):
        self.__sleep = self.__get_dictionary().getSleep()

    def set_secs_per_deg(self):
        self.__secs_per_deg = self.__get_dictionary().getSecsPerDeg()

    def set_increment_angle(self):
        self.__increment_angle = self.__get_dictionary().getIncrementAngle()

    def set_track_angle_west(self):
        self.__track_angle_west = self.__get_dictionary().getTrackAngleWest()
        self.__current_angle = self.__track_angle_west ##changeback

    def set_track_angle_east(self):
        self.__track_angle_east= self.__get_dictionary().getTrackAngleEast()
     #   self.__current_angle = self.__track_angle_east

    def set_azimuth_angle_start(self):
        self.__azimuth_angle_start = self.__get_dictionary().getAzimuthAngleStart()

    def set_azimuth_angle_stop(self):
        self.__azimuth_angle_stop = self.__get_dictionary().getAzimuthAngleStop()

    def __init__(self):
        super().__init__()
        logger = SysLog.getLogger()
        logger.debugs("init called")
        if SolarThread.__instance is not None:
            raise Exception("Only one Solar Thread allowed")
        self.__macAddr = None
        self.__current_angle = None #pretend calibrate has been called
        self.__stop_increment_angle = False
        self.__east_relay = False
        self.__west_relay = False
        self.__reset_called = False
        self.__max_angle_check = False
        self.__latitude = None
        self.__longitude = None
        self.__sleep = None
        self.__secs_per_deg = None
        self.__increment_angle = None
        self.__track_angle_west = None
        self.__track_angle_east = None
        self.AZIMUTH_TO_SOLAR_OFFSET = 180
        self.__sleep_time_for_manual_relays = .1
        self.__azimuth_angle_start = None
        self.__azimuth_angle_stop = None
        return

    #@classmethod
    def calibrate_solar_panel(self):
        self.stop_all()
        self.__stop_increment_angle = False
        time_to_move = time.time() + 900 #900  CHANGE BACK
        self.__turn_on_east_relay()
        print("calibrate on")
        while time.time() < time_to_move and self.__stop_increment_angle == False:
            print("increment angle: ", self.__stop_increment_angle)
            print("in calibrate loop:", GPIO.input(Constants.RELAY_EAST))
            if self.__current_angle < self.__track_angle_east:
                self.__current_angle = self.__track_angle_east
                self.__update_solar_animation()
            else:
                self.__current_angle = self.__current_angle + (-1*(self.__sleep/( self.__secs_per_deg)))
                self.__update_solar_animation()
            time.sleep(self.__sleep)
        self.stop_all()
        print("calibrate off")

    def setMacAddr(self, macAddr):
        print("SETMACADDR", macAddr)
        logger = SysLog.getLogger()
        logger.debugs("macAddr Solar.py: %s" % macAddr)
        self.__macAddr = macAddr

    def get_current_angle(self):
        return self.__current_angle

    def trackSolar(self):
        logger = SysLog.getLogger()
        self.__stop_increment_angle = False
#        print("This is self.__current_angle", self.__current_angle)
        while True:
 #           logger.debugs("SolarThread")
            if self.get_stop_thread():
  #              logger.debugs("THREAD STOPPED")
                self.set_stop_thread(False)
                self.set_thread(None)
                break
            current_azimuth = get_azimuth(self.__latitude, self.__longitude, SolarThread.get_time())  #gps_lat, gps_lng, current_time, 0)
   #         print("current azimuth", current_azimuth)
            new_angle = current_azimuth - self.AZIMUTH_TO_SOLAR_OFFSET # change back to 180!!!!
            if self.__track_angle_east < new_angle < self.__track_angle_west: #when we would start moving the panel
                self.__reset_called = False # reset...reset for next day
                self.__max_angle_check = False
    #            print("This is new angle: ", new_angle)
    #            print("This is current angle: ", self.__current_angle)
                difference = new_angle - self.__current_angle
     #           print("This is difference: ", difference)
                if difference >= self.__increment_angle:
     #               print("Larger than")
                    self.increment_panel_angle(difference, self.__turn_on_west_relay)
                elif difference < (-1 * self.__increment_angle):
      #              print("Smaller than")
                    self.increment_panel_angle(difference, self.__turn_on_east_relay)
                time.sleep(self.__sleep)
            elif current_azimuth > self.__azimuth_angle_stop and current_azimuth < self.__azimuth_angle_stop + 100 and not self.__max_angle_check:  #make sure panel is all the way west
       #         print("notreset")
                difference = self.__track_angle_west - self.__current_angle + Constants.ST_DEGREE_BUFFER
                self.increment_panel_angle(difference, self.__turn_on_west_relay)
                self.__max_angle_check = True
            elif (current_azimuth < self.__azimuth_angle_start or current_azimuth > self.__azimuth_angle_stop + 100) and not self.__reset_called:  #make sure panel is all the way east
        #        print("reset 0")
                difference = self.__track_angle_east - self.__current_angle - Constants.ST_DEGREE_BUFFER
                self.increment_panel_angle(difference, self.__turn_on_east_relay)
                self.__reset_called = True
            else:  #where checks have already been done
                time.sleep(self.__sleep)
         #       logger.debugs("new angle %s" %new_angle)
         #       logger.debugs("current angle %s" %self.__current_angle)

    def increment_panel_angle(self, angle_to_move, direction):  #direction is a passed method
       # print("SolarThread.__stop_increment: ", self.__stop_increment_angle)
       # print("angle to move: ", angle_to_move)
        self.__stop_increment_angle = False
        if angle_to_move + self.__current_angle > self.__track_angle_west:
          #  print( ">45")
            angle_to_move = self.__track_angle_west - self.__current_angle + Constants.ST_DEGREE_BUFFER   # +1 for good luck  find reasonable time to reach max angle
        elif angle_to_move + self.__current_angle < self.__track_angle_east:
         #   print( "<-45")
            angle_to_move = self.__track_angle_east - self.__current_angle - Constants.ST_DEGREE_BUFFER  # +1 for good luck  find reasonable time to reach max angle
        else:
            print("not either case")
        sign = direction()
        if sign == -1:
            self.__move_solar_panel_east(sign, angle_to_move)
        elif sign == 1:
            self.__move_solar_panel_west(sign, angle_to_move)
        if self.__current_angle > self.__track_angle_west:
            self.__current_angle = self.__track_angle_west
        elif self.__current_angle < self.__track_angle_east:
            self.__current_angle = self.__track_angle_east
        print(self.__current_angle)
        SolarThread.turn_off_relays()
        self.__stop_increment_angle = False

    def __move_solar_panel_east(self, sign, angle_to_move):
        newAngle = self.__current_angle + angle_to_move
        #print("new angle: ", newAngle, " current_angle: ", self.__current_angle, "stop_increment:", self.__stop_increment_angle)
        while(self.__current_angle > newAngle and not self.__stop_increment_angle):
         #   print("east: ", GPIO.input(Constants.RELAY_EAST))
            self.__move_panels(sign)

    def __move_solar_panel_west(self, sign, angle_to_move):
        newAngle = self.__current_angle + angle_to_move
        while(self.__current_angle < newAngle and not self.__stop_increment_angle):
          #  print("west: ", GPIO.input(Constants.RELAY_WEST))
            self.__move_panels(sign)

    def __move_panels(self, sign):
       # print("current angle: ", self.__current_angle)
        self.__current_angle = self.__current_angle + (sign*(self.__sleep/( self.__secs_per_deg)))  #   1 degree per 8.2, looping every half second 1/(8.2*2)
        self.__update_solar_animation()
        time.sleep(self.__sleep)

    #@classmethod
    def __update_solar_animation(self):
        if self.__current_angle > self.__track_angle_west:
            socketio.emit('rotate_panel_animation_js', self.__track_angle_west)
        elif self.__current_angle < self.__track_angle_east:
            socketio.emit('rotate_panel_animation_js', self.__track_angle_east)
        else:
            socketio.emit('rotate_panel_animation_js', self.__current_angle)

    @staticmethod
    def get_time():
        dtime = dt.now(pytz.timezone("America/Los_Angeles"))
       # print(dtime)
        return dtime #dtime.replace(tzinfo=timezone.America/Los_Angeles)

    def turn_on_west_relay_manual(self):
        self.stop_all()
        #logger = SysLog.getLogger()
        self.__stop_increment_angle = False
       # print(self.__current_angle)
       # print("self.__west_relay: ", self.__west_relay)
        while not self.__stop_increment_angle:
            if not self.__west_relay:
                self.__turn_on_west_relay()
                self.__west_relay = True
            if self.__current_angle < self.__track_angle_west: # make constant
        #        print("angle < 45")
                self.__current_angle = self.__current_angle + (self.__sleep_time_for_manual_relays/self.__secs_per_deg) # .1/(8.5)
                self.__update_solar_animation()
            else:
        #        print("angle should be 45")
                self.__current_angle = self.__track_angle_west
                self.__update_solar_animation()
        #    print("SolarThread_current_angle: ", self.__current_angle)
            time.sleep(self.__sleep_time_for_manual_relays)
        SolarThread.turn_off_relays()
        self.__west_relay = False
        self.__stop_increment_angle = False

    def turn_on_east_relay_manual(self):
        #logger = SysLog.getLogger()
        self.stop_all()
        self.__stop_increment_angle = False
      #  print(self.__current_angle)
      #  print("self.__east_relay: ", self.__east_relay)
        while not self.__stop_increment_angle:
            if not self.__east_relay:
                self.__turn_on_east_relay()
                self.__east_relay = True
            if self.__current_angle > self.__track_angle_east: # make constant
                self.__current_angle = self.__current_angle - (self.__sleep_time_for_manual_relays/self.__secs_per_deg) # .1/(8.5) == 0.0122, 82 loops is 8.2 seconds which is a total of 1 degree incremented  
                self.__update_solar_animation()
            else:
                self.__current_angle = self.__track_angle_east
                self.__update_solar_animation()
       #     print("SolarThread_current_angle: ", self.__current_angle)
            time.sleep(self.__sleep_time_for_manual_relays)
        SolarThread.turn_off_relays()
        self.__east_relay = False
        self.__stop_increment_angle = False

    def go_to_evening_position_manual(self):
        self.__stop_increment_angle = False
        difference = self.__track_angle_west - self.__current_angle + Constants.ST_DEGREE_BUFFER
        self.increment_panel_angle(difference, self.__turn_on_west_relay)
        
    def go_to_morning_position_manual(self):
        self.__stop_increment_angle = False
        difference = self.__track_angle_east - self.__current_angle - Constants.ST_DEGREE_BUFFER  # make -2 constant, to make sure device is at -45
      #  print("this is difference: ", difference)
      #  print("SolarThread.__turn on east relay", self.__turn_on_east_relay)
        self.increment_panel_angle(difference, self.__turn_on_east_relay)

    def move_to_22_degrees(self):
        self.__stop_increment_angle = False
        difference = -22 - self.__current_angle
        if difference > 0:
            self.increment_panel_angle(difference, self.__turn_on_west_relay)
        elif difference < 0:
            self.increment_panel_angle(difference, self.__turn_on_east_relay)

    def set_stop_increment_angle(self, bbool):
        self.__stop_increment_angle = bbool
    
    def __turn_on_west_relay(self):
        ### #@GPIO@#      Enable/Disable GPIO
      #  print("turn on west relay")
        if GPIO.input(Constants.RELAY_EAST):
            GPIO.output(Constants.RELAY_EAST, GPIO.LOW)
            time.sleep(self.__sleep)
        ##@GPIO@##        Enable/Disable #@GPIO@# ###
        ### #@GPIO@#      Enable/Disable GPIO
        GPIO.output(Constants.RELAY_WEST, GPIO.HIGH)
        ##@GPIO@##        Enable/Disable #@GPIO@# ###
        return 1

    def __turn_on_east_relay(self):
        ### #@GPIO@#      Enable/Disable GPIO
     #   print("turn on east relay")
        if GPIO.input(Constants.RELAY_WEST):
            GPIO.output(Constants.RELAY_WEST, GPIO.LOW)
            time.sleep(self.__sleep)
        ##@GPIO@##        Enable/Disable #@GPIO@# ###
        ### #@GPIO@#      Enable/Disable GPIO
        GPIO.output(Constants.RELAY_EAST, GPIO.HIGH)
        ##@GPIO@##        Enable/Disable #@GPIO@# ###
        return -1

    @staticmethod
    def turn_off_relays():
        ### #@GPIO@#      Enable/Disable GPIO
      #  print("turn_off_relays")
        GPIO.output(Constants.RELAY_WEST, GPIO.LOW)
        GPIO.output(Constants.RELAY_EAST, GPIO.LOW)
        ##@GPIO@##        Enable/Disable #@GPIO@# ###
        return

    def stop_all(self):
     #   print("Stop all called")
        self.set_stop_thread(True)
        self.__stop_increment_angle = True
        self.__east_relay = False
        self.__west_relay =False
        SolarThread.turn_off_relays()
        self.__max_angle_check = False
        self.__reset_called = False
        
