import sys
import time

import pygame as pg
import serial
from threading import Thread
import sys

class PTZ:
    ax = 0
    ay = 0
    port = "/dev/cu.usbserial-110"
    ard = None
    def __init__(self, port):
        self.port = port
        serial.Serial.write_timeout = 0
        self.ard = serial.Serial(port, 2000000)
        self.ard.write_timeout = 0
        #t = Thread(target=self.start_updating)
        #t.start()
        s =  self.ard.readline().decode("utf-8")
        self.ard.write_timeout = 0
        if "PTZ is ready!" in s:
            print("PTZ has inited succesfully")
        else:
            raise "Нет соединения с системой поворота"
    def start_updating(self):
        while 1:
            if abs(self.ax) > 1 or abs(self.ay) > 1:
                self.ard.write(bytes("0b " + str(self.ax) + " " + str(self.ay), "utf-8"))
                print(self.ard.readline().decode("utf-8"))
                # ddprint("0 " +str(ax) + " " + str(ay))
                self.ax = 0
                self.ay = 0
            time.sleep(0.002)
    def update(self):
        if abs(self.ax) > 1 or abs(self.ay) > 1:
            self.ard.write(bytes("0b " + str(self.ax) + " " + str(self.ay), "utf-8"))
            # ddprint("0 " +str(ax) + " " + str(ay))
            self.ax = 0
            self.ay = 0



#ptz.ard.write(bytes("0b 10 10", "utf-8"))

