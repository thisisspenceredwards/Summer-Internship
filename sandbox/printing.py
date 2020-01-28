import json
import logging
import sys
import uuid
sys.path.append('../Common')
import Constants
from Configuration import ConfigDict, ConfigListOfDict
import SysLogger

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

SysLogger.initialize(__name__, 'master.log', "%(asctime)s — %(name)s — %(levelname)s — %(message)s", logging.DEBUG)

logger = SysLogger.getLogger()

logger.info("Log Started")


myMacAddr = hex(uuid.getnode())         # hex returns a string

dhcpConfig = ConfigListOfDict()
dhcpConfig.addConfigDict(Constants.CFG_DEFAULT_DHCP_RECORD)

dhcpRec = ConfigDict(Constants.CFG_DEFAULT_DHCP_RECORD)


###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

msg = '{oc}"{s1}":"{s2}"{cc}'.format(oc='{', s1=Constants.CFG_KEY_MAC_SELF, s2=myMacAddr, cc='}')
logger.debug("Publishing::topic={}= msg={}=".format(dhcpRec.makeTopicDhcpReq(), msg))

out = []
out.append(Constants.CFG_DEFAULT_DHCP_RECORD)
print("New out::{}".format(out))


print(dhcpRec.makeTopicDhcpAllReq())
print(dhcpRec.makeTopicDhcpAllRsp())
print(dhcpRec.makeTopicDhcpReq())
print(dhcpRec.makeTopicDhcpRsp())
print(dhcpRec.makeTopicSignonReq())
print(dhcpRec.makeTopicSignonRsp())

