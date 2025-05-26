import socket
import time



HOST = "192.168.1.252"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
import datetime
from SKUD import *
import os
import pickle



file_path = os.path.dirname(os.path.abspath(__file__))
def path(p):
    return os.path.join(file_path, "server_files",  p)

is_run = True

doors = []
sensors = []
cams = []




def open_cams():
    global cams
    f = open(path("cams.data"), mode="rb")
    cams = pickle.load( f)

def open_doors():
    global doors
    f = open(path("doors.data"), mode="rb")
    doors = pickle.load( f)

def open_sensors():
    global sensors
    f = open(path("sensors.data"), mode="rb")
    sensors = pickle.load( f)

open_cams()
open_sensors()
open_doors()




def save_cams():
    f = open(path("cams.data"), mode = "wb")
    pickle.dump(cams,f)


def save_doors():
    f = open(path("doors.data"), mode = "wb")
    pickle.dump(doors,f)


def save_sensors():
    f = open(path("sensors.data"), mode = "wb")
    pickle.dump(sensors,f)



def saving():
    while is_run:
        save_cams()
        save_doors()
        save_sensors()
        time.sleep(1)

t = Thread(target=saving)
t.start()

users = [("user", "password")]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while 1:
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024)
            st = data.decode('utf-8')
            spl = st.split('\n')
            if (spl[0], spl[1]) not in users:
                conn.sendall(b"Undefined username or password")
                conn.close()
                continue

            spl = spl[2:]
            print(spl)

            if not data:
                break

            elif spl[0] == "get_time":
                conn.sendall(bytes(str(datetime.datetime.now()), "utf-8"))
            elif spl[0] == "get_cams":
                res = ''
                for i in cams:
                    res += i.name + "\n"
                conn.sendall(bytes(res, "utf-8"))
            elif spl[0] == "get_doors":
                res = ''
                for i in doors:
                    res += i.name + "\n"

                conn.sendall(bytes(res, "utf-8"))
            elif spl[0] == "get_sensors":
                res = ''
                for i in sensors:
                    res += i.name + "\n"
                conn.sendall(bytes(res, "utf-8"))



            elif spl[0] == 'get_camera':
                num = int(spl[1])
                cam = cams[num]
                res = f"{cam.name}\n{cam.location}\n{cam.ip}\n{cam.port}"
                conn.sendall(bytes(res, "utf-8"))
            elif spl[0] == "get_door":
                num = int(spl[1])
                dor = doors[num]
                res = (f"{dor.name}\n{dor.location}\n{dor.ip}\n{dor.port}\n{dor.level}")
                conn.sendall(bytes(res, "utf-8"))
            elif spl[0] == "get_sensor":
                num = int(spl[1])
                sen = sensors[num]
                res = (f"{sen.name}\n{sen.location}\n{sen.ip}\n{sen.port}")
                conn.sendall(bytes(res, "utf-8"))



            elif spl[0] == "add_camera":
                cam = camera(spl[1], spl[2], spl[3], spl[4])
                cams.append(cam)
                print(spl[1], spl[2], spl[3], spl[4])
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
                cams[num] = cam
                conn.sendall(b'ok')
            elif spl[0] == "update_door":
                dor = door(spl[1], spl[2], spl[3], spl[4], spl[5])
                print(spl[1], spl[2], spl[3], spl[4], spl[5])
                num = int(spl[6])
                doors[num] = dor
                conn.sendall(b'ok')
            elif spl[0] == "update_sensor":
                sen = sensor(spl[1], spl[2], spl[3], spl[4])
                num = int(spl[5])
                sensors[num] = sen
                conn.sendall(b'ok')

            else:
                print("error")
                print(data.decode("utf-8"))
                conn.sendall(b"Error")
                conn.close()










