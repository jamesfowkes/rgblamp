import logging
import serial
import json
import time

from flask import Blueprint, request, Response

from lampcontroller import app

api = Blueprint('api', __name__)

def get_logger():
	return logging.getLogger(__name__)

def setup_logger(handler):
    get_logger().setLevel(logging.INFO)
    get_logger().addHandler(handler)

@api.route("/api/flash/<r>/<g>/<b>/<count>")
def api_flash(r, g, b, count):

	get_logger().info("Handling /api/flash/{}/{}/{}/{}".format(r, g, b, count))
		
	command = ""
	
	if app.config["serial_port"] is not None:
	
		try:
			r, g, b, count = int(r), int(g), int(b), int(count)
		except ValueError:
			return json.dumps({"success": False})

		port = serial.Serial(app.config["serial_port"], 115200)
		
		for _ in range(count):
			command = "R{:03d}G{:03d}B{:03d}\n".format(r, g, b)
			port.write(command.encode('utf-8'))
			time.sleep(0.1)
			command = "R000G000B000\n"
			port.write(command.encode('utf-8'))
			time.sleep(0.1)
			
		port.close()

	return json.dumps(
		{
			"success": True,
			"command": command
		}
	)

@api.route("/api/<r>/<g>/<b>")
def api_set_rgb(r, g, b):

	get_logger().info("Handling /api/{}/{}/{}".format(r, g, b))
	
	command = ""
	if app.config["serial_port"] is not None:

		try:
			r, g, b = int(r), int(g), int(b)
		except ValueError:
			return json.dumps({"success": False})

		port = serial.Serial(app.config["serial_port"], 115200)
		
		command = "R{:03d}G{:03d}B{:03d}\n".format(r, g, b)

		get_logger().info("Writing {}".format(command))

		port.write(command.encode('utf-8'))
		
		port.close()

	return json.dumps(
		{
			"success": True,
			"command": command
		}
	)
