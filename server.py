import socket
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
import datetime
from SKUD import *


cameras = []
cam1 = camera("192","У входа","Входная","55")
cameras.append(cam1)
cam1 = camera("192","У входа","Выходная","55")
cameras.append(cam1)
cam1 = camera("192","У входа","Внутренняя","55")
cameras.append(cam1)
cam1 = camera("192","У входа","Внутривенная","55")
cameras.append(cam1)


doors = []
dor = door("Вход", "У входа", "", "192", "", "55")
doors.append(dor)
dor = door("Выход", "У входа", "", "192", "", "55")
doors.append(dor)

dor = door("Служебная", "У входа", "", "192", "", "55")
doors.append(dor)

dor = door("Туалет", "У входа", "", "192", "", "55")
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

            while True:

                data = conn.recv(1024)
                st = data.decode('utf-8')
                if not data:
                    break

                elif data == b"get_time":
                    conn.sendall(bytes(str(datetime.datetime.now()), "utf-8"))
                elif data == b"get_cameras":
                    res = ''
                    for i in cameras:
                        res += i.name + "\n"
                    conn.sendall(bytes(res, "utf-8"))
                elif data == b"get_doors":
                    res = ''
                    for i in  doors:
                        res += i.name + "\n"

                    conn.sendall(bytes(res, "utf-8"))
                elif data == b"get_sensors":
                    res = ''
                    for i in sensors:
                        res += i.name + "\n"

                    conn.sendall(bytes(res, "utf-8"))
                elif st.split()[0] == 'get_camera':
                    num = int(st.split()[1])
                    cam = cameras[num]
                    res = f"{cam.name}\n{cam.location}\n{cam.ip}\n{cam.port}"
                    print(res)
                    conn.sendall(bytes(res, "utf-8"))
                elif st.split()[0] == "get_door":
                    num = int(st.split()[1])
                    cam = doors[num]
                    res = (f"{cam.name}\n{cam.location}\n{cam.ip}\n{cam.port}")
                    conn.sendall(bytes(res, "utf-8"))
                elif st.split()[0] == "get_sensor":
                    num = int(st.split()[1])
                    cam = sensors[num]
                    res = (f"{cam.name}\n{cam.location}\n{cam.ip}\n{cam.port}")
                    conn.sendall(bytes(res, "utf-8"))
                else:

                    conn.sendall(b"Error")
                continue

