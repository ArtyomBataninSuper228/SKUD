# echo-client.py
import dearpygui.dearpygui as dpg
import socket

def response(host,port,data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(data)
        resp = s.recv(1024)
        return resp

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server






dpg.create_context()
dpg.create_viewport(title='Client', width=600, height=300)

def upgate(a):
    tm = str(response(HOST, PORT, b"get_time"))
    dpg.set_value(a, tm)

with dpg.window(label="Example Window"):
    dpg.add_text("Hello, world")
    id_e = dpg.last_item()
    dpg.add_button(label="Get_data", callback=lambda m, s:upgate(id_e) )
    dpg.add_input_text(label="string", default_value="Quick brown fox")
    dpg.add_slider_float(label="float", default_value=0.273, max_value=1)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()