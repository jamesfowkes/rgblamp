#!/usr/bin/python3
"""run.py

Usage:
	run.py [--mock]
"""

import socket
import os
import docopt

from sensor import Sensor

args = docopt.docopt(__doc__)

port = int(os.getenv("RGBLAMP_BUTTON_PORT"))
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', port))
server_socket.listen(5)

sensor = Sensor(args["--mock"])

while True:
    (client_socket, address) = server_socket.accept()

    button_states = sensor.get_button_states()
    states = map(lambda s: "1" if s else "0", button_states)
    states = "".join(states).encode("utf-8")
    client_socket.send(bytes(states))
