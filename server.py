import socket
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
import datetime
from SKUD import *
import os



file_path = os.path.dirname(os.path.abspath(__file__))
def path(p):
    return os.path.join(file_path, "server_files",  p)


cams = []
cam1 = camera("192","У входа","Входная","55")
cams.append(cam1)
cam1 = camera("192","У входа","Выходная","55")
cams.append(cam1)
cam1 = camera("192","У входа","Внутренняя","55")
cams.append(cam1)
cam1 = camera("192","У входа","Внутривенная","55")
cams.append(cam1)


doors = []
dor = door("Вход", "У входа", "192", "", "55")
doors.append(dor)
dor = door("Выход", "У входа", "192", "", "55")
doors.append(dor)

dor = door("Служебная", "У входа", "192", "", "55")
doors.append(dor)

dor = door("Туалет", "У входа", "192", "", "55")
doors.append(dor)


sensors = []
for i in range(10):
    sensors.append(sensor(f"Sensor no {i}", 'тут', '', ''))


def open_cams():
    pass

def save_cams():
    f = open(path("cams.txt"), mode = "w")
    res = ""
    for cam in cams:
        pass
    

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
                spl = st.split('\n')
                if not data:
                    break

                elif data == b"get_time":
                    conn.sendall(bytes(str(datetime.datetime.now()), "utf-8"))
                elif data == b"get_cams":
                    res = ''
                    for i in cams:
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



                elif spl[0] == 'get_camera':
                    num = int(st.split()[1])
                    cam = cams[num]
                    res = f"{cam.name}\n{cam.location}\n{cam.ip}\n{cam.port}"
                    conn.sendall(bytes(res, "utf-8"))
                elif spl[0] == "get_door":
                    num = int(st.split()[1])
                    dor = doors[num]
                    res = (f"{dor.name}\n{dor.location}\n{dor.ip}\n{dor.port}\n{dor.level}")
                    conn.sendall(bytes(res, "utf-8"))
                elif spl[0] == "get_sensor":
                    num = int(st.split()[1])
                    sen = sensors[num]
                    res = (f"{sen.name}\n{sen.location}\n{sen.ip}\n{sen.port}")
                    conn.sendall(bytes(res, "utf-8"))



                elif spl[0] == "add_camera":
                    cam = camera(spl[1], spl[2], spl[3], spl[4])
                    cams.append(cam)
                    conn.sendall(b'ok')
                elif spl[0] == "add_door":
                    dor = door(spl[1], spl[2], spl[3], spl[4], spl[5])
                    doors.append(dor)
                    conn.sendall(b'ok')
                elif spl[0] == "add_sensor":
                    sen = sensor(spl[1], spl[2], spl[3], spl[4])
                    sensors.append(sen)
                    conn.sendall(b'ok')



                elif spl[0] == "update_camera":
                    cam = camera(spl[1], spl[2], spl[3], spl[4])
                    num = int(spl[5])
                    cams[num]=cam
                    conn.sendall(b'ok')
                elif spl[0] == "update_door":
                    dor = door(spl[1], spl[2], spl[3], spl[4], spl[5])
                    print(spl[1], spl[2], spl[3], spl[4], spl[5])
                    num = int(spl[6])
                    doors[num]=dor
                    conn.sendall(b'ok')
                elif spl[0] == "update_sensor":
                    sen = sensor(spl[1], spl[2], spl[3], spl[4])
                    num = int(spl[5])
                    sensors[num]= sen
                    conn.sendall(b'ok')

                else:

                    conn.sendall(b"Error")
                continue

