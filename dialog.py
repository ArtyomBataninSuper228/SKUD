import sys

import pygame as pg
import serial
import math
print(math.atan((5/54)**0.5)/math.pi*180, 2.4**2)



ard = serial.Serial("COM3", 2000000)



sc = pg.display.set_mode((100, 100))
ax = 0
ay = 0
def f():
    global ax, ay
    ard.write(bytes(str(ax), "utf-8"))
    ard.write(bytes(str(ay)), "utf-8")
while 1:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            sys.exit()
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_w:
                ay = 10
            elif e.key == pg.K_s:
                ay = -10

        if e.key == pg.K_d:
            ax = 10
        elif e.key == pg.K_a:
            ax = -10