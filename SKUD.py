from PTZ import *
import socket
import logging


class camera:
    def __init__(self, ip, location, name, port):
        self.ip = ip
        self.location = location
        self.name = name
        self.port = port
        self.ptz_sys = PTZ(self.port)

    def start_detecting(self):
        pass

class door:
    def __init__(self, name, location, is_opened, ip, level, port):
        self.name = name
        self.location = location
        self.is_opened = is_opened
        self.ip = ip
        self.level = level
        self.port = port

    def open(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.ip, self.port))
            s.sendall(b"Open the door")
            resp = s.recv(1024)
            return resp



