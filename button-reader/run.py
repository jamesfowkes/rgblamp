#!/usr/bin/python3
import socket
import os

from Adafruit_MPR121 import MPR121

sensor = MPR121.MPR121()
sensor.begin()

def get_button_states():	
    return [sensor.is_touched(i) for i in range(6)]

port = int(os.getenv("RGBLAMP_BUTTON_PORT"))
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((socket.gethostname(), port))
server_socket.listen(5)

while True:
    (client_socket, address) = server_socket.accept()

    button_states = get_button_states()
    states = map(lambda s: "1" if s else "0", button_states)
    states = "".join(states).encode("utf-8")
    client_socket.send(bytes(states))
