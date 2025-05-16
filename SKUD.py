from PTZ import *
class camera:
    def __init__(self, ip, location, name, port):
        self.ip = ip
        self.location = location
        self.name = name
        self.port = port
        PTZ = ptz(self.port)