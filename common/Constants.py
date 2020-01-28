
######################################################################
""" Constants.py :: Contains all the (global) constants """
""" force put """
CFG_MQTT_SUBSCRIBE_ALL = '#'

CFG_FILE_PATH = '/home/pi/raspberry30/slave2/'
CFG_FILE_NAME_DHCP    = 'dhcpConfig.json'
CFG_FILE_NAME_STARTUP = 'startupBroker.json'

CFG_FILE_NAME_DEBUG_DHCP    = 'debugDhcpConfig.json'
CFG_FILE_NAME_DEBUG_MASTER  = 'debugMasterConfig.json'
CFG_FILE_NAME_DEBUG_MONITOR = 'debugMonitorConfig.json'
CFG_FILE_NAME_DEBUG_SLAVE   = 'debugSlaveConfig.json'


ICON_GREEN_DOT = "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
ICON_BLUE_DOT = "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"

"""
NOTE:
    For every DHCP entry, create 
        1 -- a constant for each KEY
        2 -- a constant for every known value
        3 -- an entry in the DEFAULT DHCP Dictionary

Tracking the sun:
There are three values that are used to control tracking the sun:

1) The total number of seconds to move the full range of motion from east to west.
2) The maximum angle of the panels to the east.  This is the starting position of the 
   panels in the morning. This is a negative number.
3) The maximum angle of the panels to the west.  This is the ending position of the 
   panels at the end of the day.  This is a positive number.

These angles are relative to the eastern horizon.  An angle of 0 degrees is when the 
panels are tangent to the earth's surface.  That is, the panels are horizontal:  a bubble 
on a level placed on a panel would be in the center showing that the panel is level.  
When the panels are tilted toward the east, the angle is less than 0.  When the panels are 
tilted to the west, the angle is greater than 0.

CFG_KEY_TRACK_TIME_SECS
    The total time in seconds to move from the minimum tracking angle to the 
    maximum tracking angle
CFG_KEY_TRACK_ANGLE_EAST
    The eastern most angle of the panels.  A negative number.
CFG_KEY_TRACK_ANGLE_WEST
    The western most angle of the panels.  A positive number.

"""

#CFG_KEY_INFOBOX          = "infobox"
CFG_KEY_COMMAND          = "command"
CFG_KEY_COMMENT          = "comment"
CFG_KEY_GPS              = "gps"
CFG_KEY_PORT_BROKER      = "brokerPort"
CFG_KEY_PORT_HTTP        = "httpPort"
CFG_KEY_ICON             = "icon"
CFG_KEY_IP_ADDR          = "ipAddr"
CFG_KEY_LAT              = "lat"
CFG_KEY_LNG              = "lng"
CFG_KEY_MAC_MASTER       = "macMaster"
CFG_KEY_MAC_SELF         = "macSelf"
CFG_KEY_MQ_PUB           = "mqPub"
CFG_KEY_MQ_SUB           = "mqSub"
CFG_KEY_MSG_FIRST        = "msgFirst"
CFG_KEY_MSG_LAST         = "msgLast"
CFG_KEY_SYS_STATUS       = "sysStatus"
CFG_KEY_SYS_NAME         = "sysName"
CFG_KEY_SYS_TYPE         = "sysType"
CFG_KEY_TITLE            = "title"
CFG_KEY_TOPIC_ROOT       = "topicRoot"
CFG_KEY_TRACK_TIME_SECS  = "trackTimeSecs"
CFG_KEY_TRACK_ANGLE_EAST = "trackAngleEast"
CFG_KEY_TRACK_ANGLE_WEST = "trackAngleWest"
CFG_KEY_SLEEP            = "sleep"
CFG_KEY_LATITUDE         = "latitude"
CFG_KEY_LONGITUDE        = "longitude"
CFG_KEY_INCREMENT_ANGLE  = "increment_angle"
CFG_KEY_AZIMUTH_ANGLE_START = "azimuth_angle_start"
CFG_KEY_AZIMUTH_ANGLE_STOP  = "azimuth_angle_stop"


CFG_VALUE_SYS_TYPE_BROKER  = "broker"
CFG_VALUE_SYS_TYPE_DHCP    = "dhcp"
CFG_VALUE_SYS_TYPE_ERROR   = "error"
CFG_VALUE_SYS_TYPE_MASTER  = "master"
CFG_VALUE_SYS_TYPE_MONITOR = "monitor"
CFG_VALUE_SYS_TYPE_SLAVE   = "slave"

CFG_VALUE_DEFAULT_GPS                 = "0.0,0.0"
CFG_VALUE_DEFAULT_PORT_BROKER         = 1883
CFG_VALUE_DEFAULT_PORT_HTTP           = 5000
CFG_VALUE_DEFAULT_ICON                = ICON_BLUE_DOT
CFG_VALUE_DEFAULT_IP                  = "0.0.0.0"
CFG_VALUE_DEFAULT_FLOAT               = "0.0"
CFG_VALUE_DEFAULT_HEX                 = 0
CFG_VALUE_DEFAULT_INT                 = 0
CFG_VALUE_DEFAULT_STRING              = ""
CFG_VALUE_DEFAULT_CONNECT             = "connect"
CFG_VALUE_DEFAULT_TRACK_TIME          =  789.9 # 13minutes 9 seconds 9 miliseconds
CFG_VALUE_DEFAULT_TRACK_ANGLE_EAST    = -47.5
CFG_VALUE_DEFAULT_TRACK_ANGLE_WEST    = 40
CFG_VALUE_DEFAULT_SLEEP               = .5
CFG_VALUE_DEFAULT_LATITUDE            = 38.164570
CFG_VALUE_DEFAULT_LONGITUDE           = -120.957934
CFG_VALUE_DEFAULT_INCREMENT_ANGLE     = 1
CFG_VALUE_DEFAULT_AZIMUTH_ANGLE_START = 180 + CFG_VALUE_DEFAULT_TRACK_ANGLE_EAST
CFG_VALUE_DEFAULT_AZIMUTH_ANGLE_STOP   = 180 + CFG_VALUE_DEFAULT_TRACK_ANGLE_WEST



CFG_DEFAULT_DHCP_RECORD = {
    CFG_KEY_COMMAND            : CFG_VALUE_DEFAULT_STRING              ,
    CFG_KEY_COMMENT            : CFG_VALUE_DEFAULT_STRING              ,
    CFG_KEY_GPS                : CFG_VALUE_DEFAULT_GPS                 ,
    CFG_KEY_PORT_BROKER        : CFG_VALUE_DEFAULT_PORT_BROKER         ,
    CFG_KEY_PORT_HTTP          : CFG_VALUE_DEFAULT_PORT_HTTP           ,
    CFG_KEY_ICON               : CFG_VALUE_DEFAULT_ICON                ,
    CFG_KEY_IP_ADDR            : CFG_VALUE_DEFAULT_IP                  ,
    CFG_KEY_LAT                : CFG_VALUE_DEFAULT_FLOAT               ,
    CFG_KEY_LNG                : CFG_VALUE_DEFAULT_FLOAT               ,
    CFG_KEY_MAC_MASTER         : CFG_VALUE_DEFAULT_HEX                 ,
    CFG_KEY_MAC_SELF           : CFG_VALUE_DEFAULT_HEX                 ,
    CFG_KEY_MQ_PUB             : CFG_VALUE_DEFAULT_STRING              ,
    CFG_KEY_MQ_SUB             : CFG_VALUE_DEFAULT_STRING              ,
    CFG_KEY_MSG_FIRST           : CFG_VALUE_DEFAULT_INT                ,
    CFG_KEY_MSG_LAST            : CFG_VALUE_DEFAULT_INT                ,
    CFG_KEY_SYS_STATUS          : CFG_VALUE_DEFAULT_STRING             ,
    CFG_KEY_SYS_NAME            : CFG_VALUE_DEFAULT_STRING             ,
    CFG_KEY_SYS_TYPE            : CFG_VALUE_DEFAULT_STRING             ,
    CFG_KEY_TITLE               : CFG_VALUE_DEFAULT_STRING             ,
    CFG_KEY_TOPIC_ROOT          : CFG_VALUE_DEFAULT_STRING             ,
    CFG_KEY_TRACK_TIME_SECS     : CFG_VALUE_DEFAULT_TRACK_TIME         ,
    CFG_KEY_TRACK_ANGLE_EAST    : CFG_VALUE_DEFAULT_TRACK_ANGLE_EAST   ,
    CFG_KEY_TRACK_ANGLE_WEST    : CFG_VALUE_DEFAULT_TRACK_ANGLE_WEST   ,
    CFG_KEY_SLEEP               : CFG_VALUE_DEFAULT_SLEEP              ,
    CFG_KEY_LATITUDE            : CFG_VALUE_DEFAULT_LATITUDE           ,
    CFG_KEY_LONGITUDE           : CFG_VALUE_DEFAULT_LONGITUDE          ,
    CFG_KEY_INCREMENT_ANGLE     : CFG_VALUE_DEFAULT_INCREMENT_ANGLE    ,
    CFG_KEY_AZIMUTH_ANGLE_START : CFG_VALUE_DEFAULT_AZIMUTH_ANGLE_START,
    CFG_KEY_AZIMUTH_ANGLE_STOP  : CFG_VALUE_DEFAULT_AZIMUTH_ANGLE_STOP
}

######################################################################


#Solar thread constants
ST_TIME_WAIT_SHORT = 3
ST_ANGLE = 1
ST_LATITUDE = 38.164570
ST_LONGITUDE = -120.957934
#ST_MOVE_5_DEGREES = 42
ST_MOVE_1_DEGREE = 8.2
ST_SECOND_BUFFER = 20
ST_DEGREE_BUFFER = 5
RELAY_CNTRL_SLEEP_TIME = 1
RELAY_CNTRL_MAX_ANGLE_TIME_HORIZONTAL = 294
RELAY_CNTRL_MAX_ANGLE_TIME_VERTICAL = 42
RELAY_CHANGE_DELAY = 2
RELAY_WEST = 23
RELAY_EAST = 22
RELAY_NUM_OF_TIMES = 42

###
