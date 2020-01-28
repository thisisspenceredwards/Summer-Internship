""" rPiConfig -- Creates DHCP configuration file for the Raspberries """
import sys
try:
    sys.path.append('../common')
    import Constants
except ImportError:
    sys.path.append('/home/pi/raspberry20/common')
    import Constants
#from ConfigReaderWriter import ConfigReaderWriter
from ConfigReaderWriter import ConfigReaderWriter

##############################################################################
##############################################################################
##############################################################################
##############################################################################

"""
    Configuration is a list of dictionaries 
    MAC Address is primary key for each dictionary
    MAC Address is unique
    MAC Address is a hex string
    Only one dictionary per MAC address
    Order entries in the list by MAC address
    Use camel casing for key names and values
"""

rPiConfig = [
    {
        "0000":"OK: this is DHCP on oznog",
        "command":"",
        "comment":"",
        "gps":"38.1644611,-120.9582994",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"",
        "macSelf":"78e3b5af8cbb",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"dhcp",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK valid master on oznog",
        "command":"",
        "comment":"",
        "gps":"38.1644611,-120.9582994",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"",
        "macSelf":"78e3b5af8cbb",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"master",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK valid slave on oznog",
        "command":"",
        "comment":"",
        "gps":"38.1644611,-120.9582994",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"78e3b5af8cbb",
        "macSelf":"78e3b5af8cbb",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK iono-uno",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"78e3b5af8cbb",
        "macSelf":"b827eb5a107e",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK iono-uno master",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"",
        "macSelf":"b827eb5a107e",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"master",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK iono-uno slave",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"b827eb5a107e",
        "macSelf":"b827eb5a107e",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"Valid slave on rPi32",
        "command":"",
        "comment":"",
        "gps":"0.0,0.0",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"0.0",
        "lng":"0.0",
        "macMaster":"78e3b5af8cbb",
        "macSelf":"b827eb4a7291",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysStatus":"",
        "sysName":"",
        "sysType":"slave",
        "title":"",
        "topicRoot":"",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "command":"",
        "comment":"",
        "gps":"0.0,0.0",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"0.0",
        "lng":"0.0",
        "macMaster":"",
        "macSelf":"b827eb4a7291",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysStatus":"",
        "sysName":"raspberrypi",
        "sysType":"master",
        "title":"",
        "topicRoot":"",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"Valid slave on rPi3TS",
        "command":"",
        "comment":"",
        "gps":"0.0,0.0",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"0.0",
        "lng":"0.0",
        "macMaster":"78e3b5af8cbb",
        "macSelf":"b827eb72f292",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysStatus":"",
        "sysName":"rPi3TS",
        "sysType":"slave",
        "title":"",
        "topicRoot":"",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"Valid slave on rPi4",
        "command":"",
        "comment":"Updated record from slave",
        "gps":"0.0,0.0",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"0.0",
        "lng":"0.0",
        "macMaster":"78e3b5af8cbb",
        "macSelf":"dca63206b32d",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysStatus":"",
        "sysName":"rPi4",
        "sysType":"slave",
        "title":"",
        "topicRoot":"",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK dummy slave 0 with iono-uno master",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"78e3b5af8cbb",
        "macSelf":"00000",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK dummy slave 0 with iono-uno master",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"b827eb5a107e",
        "macSelf":"00000",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK dummy slave 1",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"78e3b5af8cbb",
        "macSelf":"00001",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK dummy slave 1",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"b827eb5a107e",
        "macSelf":"00001",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK dummy slave 2",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"78e3b5af8cbb",
        "macSelf":"00002",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK dummy slave 2",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"b827eb5a107e",
        "macSelf":"00002",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK dummy slave 3",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"78e3b5af8cbb",
        "macSelf":"00003",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK dummy slave 3",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"b827eb5a107e",
        "macSelf":"00003",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK dummy slave 4",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"78e3b5af8cbb",
        "macSelf":"00004",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK dummy slave 4",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"b827eb5a107e",
        "macSelf":"00004",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK dummy slave 5",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"78e3b5af8cbb",
        "macSelf":"00005",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK dummy slave 6",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"78e3b5af8cbb",
        "macSelf":"00006",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK dummy slave 7",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"78e3b5af8cbb",
        "macSelf":"00007",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK dummy slave 8",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"78e3b5af8cbb",
        "macSelf":"00008",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK: broker on rPi3-1 at window",
        "command":"",
        "comment":"",
        "gps":"38.1644611,-120.9582994",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"192.168.1.4",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"",
        "macSelf":"b827eb5b08f7",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"1564588416",
        "msgLast":"1564588416",
        "sysName":"",
        "sysStatus":"",
        "sysType":"broker",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK: broker on iono-due at window",
        "command":"",
        "comment":"",
        "gps":"38.1644611,-120.9582994",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"192.168.1.23",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"",
        "macSelf":"b827eb5b08f7",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"1564588416",
        "msgLast":"1564588416",
        "sysName":"",
        "sysStatus":"",
        "sysType":"broker",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK: slave on iono-due at window",
        "command":"",
        "comment":"",
        "gps":"38.1644611,-120.9582994",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"78e3b5af8cbb",
        "macSelf":"b827eb5b08f7",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "command":"",
        "comment":"",
        "gps7":"38.1644611,-120.9582994",
        "gps":"38.16446117,-120.95829947",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"192.168.1.21",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"",
        "macSelf":"78e3b5af8cbb-07",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"rPi-008",
        "sysStatus":"",
        "sysType":"monitor",
        "title7":"38.1644611,-120.9582994",
        "title":"38.16446117,-120.95829947",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"Dummy",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"b827eb5a107e",
        "macSelf":"abcdefghijklm",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK dummy slave 5",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"b827eb5a107e",
        "macSelf":"00005",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK dummy slave 6",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"b827eb5a107e",
        "macSelf":"00006",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK dummy slave 7",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"78e3b5af8cbb",
        "macSelf":"00007",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    },
    {
        "0000":"OK dummy slave 8",
        "command":"",
        "comment":"",
        "gps":"38.16446116,-120.95829946",
        "brokerPort":1883,
        "httpPort":5000,
        "icon":"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        "ipAddr":"",
        "lat":"38.1644611",
        "lng":"-120.9582994",
        "macMaster":"b827eb5a107e",
        "macSelf":"00008",
        "mqPub":"",
        "mqSub":"",
        "msgFirst":"",
        "msgLast":"",
        "sysName":"",
        "sysStatus":"",
        "sysType":"slave",
        "title":"38.1644611,-120.9582994",
        "topicRoot":"root",
        "trackTimeSecs":300,
        "trackAngleEast":-45,
        "trackAngleWest":45
    }
]

##############################################################################
##############################################################################
##############################################################################
##############################################################################

def debugSetLatLngForMacAddr(lofd, macAddr, lat, lng):
    #logger.debug("debugSetLatLngForMacAddr BEGIN")
    for dct in lofd:
        if dct[Constants.CFG_KEY_MAC_SELF] == macAddr:
            dct[Constants.CFG_KEY_LAT]   = str(lat)
            dct[Constants.CFG_KEY_LNG]   = str(lng)
            dct[Constants.CFG_KEY_GPS]   = str(lat) + ',' + str(lng)
            dct[Constants.CFG_KEY_TITLE] = dct[Constants.CFG_KEY_GPS]

            #jstr = json.dumps(dct, indent=4, separators=(',', ':'))
            #logger.debug("DCT: %s", jstr)
    #logger.debug("debugSetLatLngForMacAddr END")
    return



debugLat =   38.1644611
debugLng = -120.9582994
debugLatDelta = 0.0000200
debugLngDelta = 0.0000200
debugCalcLat = debugLat
debugCalcLng = debugLng

def debugSetLatLngInList(lofd):
    #logger.debug("debugSetLatLngInCLofD BEGIN")

    global debugCalcLat, debugCalcLng
    debugCalcLat = round(debugCalcLat, 7)
    debugCalcLng = round(debugCalcLng, 7)

    for dct in lofd:
        dct[Constants.CFG_KEY_LAT]   = str(debugCalcLat)
        dct[Constants.CFG_KEY_LNG]   = str(debugCalcLng)
        dct[Constants.CFG_KEY_GPS]   = str(debugCalcLat) + ',' + str(debugCalcLng)
        dct[Constants.CFG_KEY_TITLE] = dct[Constants.CFG_KEY_GPS]

    debugCalcLat = debugCalcLat + debugLatDelta
    debugCalcLng = debugCalcLng + debugLngDelta

    return lofd

def debugAppendToList(tol, froml):
    for dct in froml:
        tol.append(dct)
    return tol

def debugFindInList(lofd, macAddr):
    lst = []
    for dct in lofd:
        if dct[Constants.CFG_KEY_MAC_SELF] == macAddr:
            lst.append(dct)
    return lst

def removeFromList(lst, macAddr):
    found = True
    while found:
        found = False
        for dct in lst:
            if dct[Constants.CFG_KEY_MAC_SELF] == macAddr:
                lst.remove(dct)
                found = True

def updateLofd(lofd):
    #               1234567
    out = []
    more = True
    while more:
        more = False
        for dct in lofd:
            macAddr = dct[Constants.CFG_KEY_MAC_SELF]
            lst = debugFindInList(lofd, macAddr)
            debugSetLatLngInList(lst)
            debugAppendToList(out, lst)
            removeFromList(lofd, macAddr)
            more = True
            break
    return out

##############################################################################
##############################################################################
##############################################################################
##############################################################################

rPiConfig = updateLofd(rPiConfig)

rw = ConfigReaderWriter()

jstr = rw.write(rPiConfig)

print("Original indented JSON string ==", jstr)

dupConfig = rw.read()

if rPiConfig == dupConfig :
    print("Config file write/read matches")
    #print(rPiConfig)
else:
    print("ERROR:: Config files don't match")
    print("Original =")
    print(rPiConfig)
    print("")
    print("DupDict=")
    print(dupConfig)

#if __name__ == '__main__':

###
