"""
	Get this system's host name and IP address
	Found this in a web search.  It actually works.

	QUESTION:
	Is there a direct call to get the IP address?

"""	

import socket 
import uuid
  
def get_Host_name_IP(): 
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name) 
        print("Hostname :  ", host_name) 
        print("Host IP  :  ", host_ip)
        print("MAC      :  ", hex(uuid.getnode()))
    except: 
        print("Unable to get Hostname and IP") 
  

get_Host_name_IP() #Function call 
	