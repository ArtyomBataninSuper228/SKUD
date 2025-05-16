# echo-client.py
import dearpygui.dearpygui as dpg
import socket
import screeninfo



def response(host,port,data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(data)
        resp = s.recv(1024)
        return resp

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server






dpg.create_context()
dpg.create_viewport(x_pos=0,y_pos=0,title='Client',width = int(screeninfo.get_monitors()[0].width),height = int(screeninfo.get_monitors()[0].height))


text_size = 20

with dpg.font_registry():

    with dpg.font("Domino Italic.otf", text_size) as font_domino:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    with dpg.font("Domino Italic.otf", text_size + 10) as big_font_domino:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font(font_domino)
#312313
def upgate(a):
    tm = str(response(HOST, PORT, b"get_time"))
    dpg.set_value(a, tm)

def cameras_callback(sender, data):
    with dpg.window(width=300, height=300):
        number_camera=cameras.index(data)
        s = response(HOST, PORT, bytes(f'get_camera {number_camera}', 'utf8')).decode('utf-8')
        dpg.add_text(s)
        dpg.add_text(data)
        id_w = dpg.last_item()
def doors_callback(sender, data):
    with dpg.window(width=300, height=300):
        number_door=cameras.index(data)
        s = response(HOST, PORT, bytes(f'get_doors {number_door}', 'utf8')).decode('utf-8')
        dpg.add_text(s)
        dpg.add_text(data)
        id_w = dpg.last_item()
def sensors_callback(sender, data):
    with dpg.window(width=300, height=300):
        number_sensor=cameras.index(data)
        s=response(HOST, PORT, bytes(f'get_sensors {number_sensor}','utf8')).decode('utf-8')
        dpg.add_text(s)
        dpg.add_text(data)
        id_w = dpg.last_item()


cameras = response(HOST, PORT, b"get_cameras").decode("utf-8").split("\n")
doors = response(HOST, PORT, b"get_doors").decode("utf-8").split("\n")
sensors = response(HOST, PORT, b"get_sensors").decode("utf-8").split("\n")
print(cameras)
with dpg.window(width = int(screeninfo.get_monitors()[0].width),height = int(screeninfo.get_monitors()[0].height), no_title_bar=True, pos=(0, 0), no_move=True, no_resize=True, tag="Window", no_collapse= True, no_bring_to_front_on_focus=True):
    with dpg.group(horizontal=True):
        dpg.add_text("Hello, world")
        id_e = dpg.last_item()
        dpg.add_button(label="Get_data", callback=lambda m, s:upgate(id_e) )
    dpg.add_input_text(label="string", default_value="Quick brown fox")
    dpg.add_slider_float(label="float", default_value=0.273, max_value=1)
    #1
    with dpg.group(horizontal=True):
        dpg.add_listbox(cameras,num_items=15,width=400,label="Tabs",callback=lambda m, s:cameras_callback(m,s))
        dpg.add_listbox(doors, num_items=15,width=400, label="Tabs",callback=lambda m, s:doors_callback(m,s))
        dpg.add_listbox(sensors, num_items=15,width=400, label="Tabs",callback=lambda m, s:sensors_callback(m,s))

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()