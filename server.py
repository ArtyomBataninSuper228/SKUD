import socket
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
import datetime
from SKUD import *


cameras = []
cam1 = camera("","","Входная","")
cameras.append(cam1)
cam1 = camera("","","Выходная","")
cameras.append(cam1)
cam1 = camera("","","Внутренняя","")
cameras.append(cam1)
cam1 = camera("","","Внутривенная","")
cameras.append(cam1)


doors = []
dor = door("Вход", "", "", "", "", "")
doors.append(dor)
dor = door("Выход", "", "", "", "", "")
doors.append(dor)

dor = door("Служебная", "", "", "", "", "")
doors.append(dor)

dor = door("Туалет", "", "", "", "", "")
doors.append(dor)


sensors = []
for i in range(10):
    sensors.append(sensor(f"Sensor no {i}", '', '', '', ''))



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while 1:
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            print(conn)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                elif data == b"get_time":
                    conn.sendall(bytes(str(datetime.datetime.now()), "utf-8"))
                elif data == b"get_cameras":
                    res = ''
                    for i in cameras:
                        res += i.name + " "
                    print(res)
                    conn.sendall(bytes(res, "utf-8"))
                elif data == b"get_doors":
                    res = ''
                    for i in  doors:
                        res += i.name + " "
                    print(res)
                    conn.sendall(bytes(res, "utf-8"))
                elif data == b"get_sensors":
                    res = ''
                    for i in sensors:
                        res += i.name + " "
                    print(res)
                    conn.sendall(bytes(res, "utf-8"))
                else:

                    conn.sendall(b"Error")
                continue

