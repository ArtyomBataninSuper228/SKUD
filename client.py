# echo-client.py
import time

import dearpygui.dearpygui as dpg
import socket
import screeninfo
from pandas.core.dtypes.inference import is_re
from pygame.examples.midi import null_key
from threading import Thread
import os
from logging import *








### Бэкенд

file_path = os.path.dirname(os.path.abspath(__file__))
def path(p):
    return os.path.join(file_path, "client_files",  p)





basicConfig(level=INFO, filename=path("Latest_log.txt"),filemode="w")

### Нормальные настройки, все необходимые параметры добавляй в файл
settings = {}
def read_settings():
    global settings
    try:
        file_settings = open(path("settings.txt"), mode='r')
    except FileNotFoundError:
        critical(f"Файл с настройками не найден по адресу {path("settings.txt")}")
        raise f"Файл с настройками не найден по адресу {path("settings.txt")}"
    for i in file_settings.readlines():
        try:
            m = i.split("=")
            settings[m[0]] = m[1][:-1]
        except:
            warning(f"Can't read a line {i}. This line will be ignored")
    file_settings.close()

def save_settings():
    global settings
    try:
        file_settings = open(path("settings.txt"), mode='w')
    except:
        critical("Не удалось создать файл с настройками")
        raise "Не удалось создать файл с настройками"
    res = ""
    for key in settings.keys():
        s = f"{key}={settings[key]}\n"
        res += s
    file_settings.write(res)
    file_settings.close()
read_settings()



HOST = settings["host"]  # The server's hostname or IP address
PORT = int(settings["port"])  # The port used by the server


def response(host,port,data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(data)
        resp = s.recv(1024)
        return resp


### Фронтенд
is_run = True
dpg.create_context()
dpg.create_viewport(x_pos=0,y_pos=0,title='Client',width = int(screeninfo.get_monitors()[0].width),height = int(screeninfo.get_monitors()[0].height))





### Регистрация шрифтов
text_size = int(settings["textsz"])
with dpg.font_registry():
    with dpg.font("Domino Italic.otf", text_size) as font_domino:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    with dpg.font("Domino Italic.otf", text_size + 10) as big_font_domino:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font(font_domino)





def upgate(a):
    tm = str(response(HOST, PORT, b"get_time"))
    dpg.set_value(a, tm)

def cameras_callback(sender, data):
    if data=='+':
        with dpg.window(width=300, height=300):
            def add_camera(a,b):
                id=a
                name=dpg.get_value(id-4)
                locate = dpg.get_value(id-3)
                ip = dpg.get_value(id-2)
                port = dpg.get_value(id-1)
                response(HOST, PORT, bytes(f'add_camera\n{ip}\n{locate}\n{name}\n{port}','utf8'))
            dpg.add_input_text(hint='Введите название')
            dpg.add_input_text(hint='Введите расположение')
            dpg.add_input_text(hint='Введите ip')
            dpg.add_input_text(hint='Введите порт')

            dpg.add_button(label='Добавить',callback=lambda a,b:add_camera(a,b))
    else:
        with dpg.window(width=300, height=300):
            number_camera=cameras.index(data)
            s = response(HOST, PORT, bytes(f'get_camera\n{number_camera}', 'utf8')).decode('utf-8')
            dpg.add_text('Название: ' + s.split('\n')[0])
            dpg.add_text('Расположение: ' + s.split('\n')[1])
            dpg.add_text('ip: ' + s.split('\n')[2])
            dpg.add_text('Порт: ' + s.split('\n')[3])
def doors_callback(sender, data):
    if data == '+':
        with dpg.window(width=300, height=300):
            def add_door(a, b):
                id = a
                name = dpg.get_value(id - 5)
                locate = dpg.get_value(id - 4)
                level = dpg.get_value(id - 3)
                ip = dpg.get_value(id - 2)
                port = dpg.get_value(id - 1)
                response(HOST, PORT, bytes(f'add_door\n{name}\n{locate}\n{ip}\n{level}\n{port}', 'utf8'))


            dpg.add_input_text(hint='Введите название')
            dpg.add_input_text(hint='Введите расположение')
            dpg.add_input_text(hint='Введите уровень')
            dpg.add_input_text(hint='Введите ip')
            dpg.add_input_text(hint='Введите порт')

            dpg.add_button(label='Добавить', callback=lambda a, b: add_door(a, b))

    else:
        with dpg.window(width=300, height=300):
            number_door=doors.index(data)
            s = response(HOST, PORT, bytes(f'get_door\n{number_door}', 'utf8')).decode('utf-8')
            dpg.add_text('Название: '+s.split('\n')[0])
            dpg.add_text('Расположение: '+s.split('\n')[1])
            dpg.add_text('ip: ' + s.split('\n')[2])
            dpg.add_text('Порт: ' + s.split('\n')[3])
def sensors_callback(sender, data):
    if data == '+':
        with dpg.window(width=300, height=300):
            def add_door(a, b):
                id = a
                name = dpg.get_value(id - 4)
                locate = dpg.get_value(id - 3)
                ip = dpg.get_value(id - 2)
                port = dpg.get_value(id - 1)
                response(HOST, PORT, bytes(f'add_sensor\n{ip}\n{locate}\n{name}\n{port}', 'utf8'))

            dpg.add_input_text(hint='Введите название')
            dpg.add_input_text(hint='Введите расположение')
            dpg.add_input_text(hint='Введите ip')
            dpg.add_input_text(hint='Введите порт')

            dpg.add_button(label='Добавить', callback=lambda a, b: add_door(a, b))

    else:
        with dpg.window(width=300, height=300):
            number_sensor=sensors.index(data)
            s=response(HOST, PORT, bytes(f'get_sensor\n{number_sensor}','utf8')).decode('utf-8')
            dpg.add_text('Название: ' + s.split('\n')[0])
            dpg.add_text('Расположение: ' + s.split('\n')[1])
            dpg.add_text('ip: ' + s.split('\n')[2])
            dpg.add_text('Порт: ' + s.split('\n')[3])



cameras = response(HOST, PORT, b"get_cameras").decode("utf-8").split("\n")
doors = response(HOST, PORT, b"get_doors").decode("utf-8").split("\n")
sensors = response(HOST, PORT, b"get_sensors").decode("utf-8").split("\n")

cameras.pop(-1)
doors.pop(-1)
sensors.pop(-1)
cameras.append('+')
doors.append('+')
sensors.append('+')

def updating_units():
    global cameras, doors, sensors
    while is_run:
        cameras = response(HOST, PORT, b"get_cameras").decode("utf-8").split("\n")
        doors = response(HOST, PORT, b"get_doors").decode("utf-8").split("\n")
        sensors = response(HOST, PORT, b"get_sensors").decode("utf-8").split("\n")
        cameras.pop(-1)
        doors.pop(-1)
        sensors.pop(-1)
        cameras.append('+')
        doors.append('+')
        sensors.append('+')

        dpg.configure_item("cameras", items=cameras)
        dpg.configure_item("doors", items=doors)
        dpg.configure_item("sensors", items=sensors)
        time.sleep(0.5)


def open_settings():
    with dpg.window(label="Настройки", width=300):
        start_tag = dpg.last_item()
        red = 255
        green = 255
        blue = 0
        d = 255/len(settings.keys())
        for key in settings.keys():
            with dpg.group(horizontal=True):
                dpg.add_text(key, color=(red, green, blue))
                dpg.add_input_text(default_value=settings[key])
                blue += d
                red -= d
        def update_set():
            global settings
            ln = len(settings.keys())
            settings = {}
            for i in range(ln):
                key = dpg.get_value(start_tag + i*3 + 2)
                value = dpg.get_value(start_tag + i*3 + 3)
                settings[key] = value
            save_settings()
        dpg.add_button(label="Сохранить", callback=update_set)





with dpg.window(width = int(screeninfo.get_monitors()[0].width),height = int(screeninfo.get_monitors()[0].height), no_title_bar=True, pos=(0, 0), no_move=True, no_resize=True, tag="Window", no_collapse= True, no_bring_to_front_on_focus=True):
    with dpg.menu_bar():
        dpg.add_menu_item(label = "Настройки",callback=lambda a, s:open_settings())
        dpg.add_menu_item(label="Просмотреть статистику")
        dpg.add_menu_item(label="Сменить пользователя")
    with dpg.group(horizontal=True):
        dpg.add_listbox(cameras,num_items=15,width=400,callback=lambda m, s:cameras_callback(m,s), tag = "cameras")
        dpg.add_listbox(doors, num_items=15,width=400,callback=lambda m, s:doors_callback(m,s), tag = "doors")
        dpg.add_listbox(sensors, num_items=15,width=400,callback=lambda m, s:sensors_callback(m,s), tag = "sensors")





dpg.setup_dearpygui()
dpg.show_viewport()
t1 = Thread(target=updating_units)
t1.start()
dpg.start_dearpygui()

is_run = False
dpg.destroy_context()