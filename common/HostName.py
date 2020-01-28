""" HostName

    Get this system's host name

"""

import socket 


class HostName: 

    def __init__(self):
        self._name = socket.gethostname() 

    def get(self):
        return self._name

    @staticmethod
    def test():
        h = HostName()
        print("Hostname :  ", h.get())


if __name__ == '__main__':
    HostName.test()


###
