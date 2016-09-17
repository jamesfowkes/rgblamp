import logging
import serial
import json

from flask import Blueprint, request, Response

from lampcontroller import app

api = Blueprint('api', __name__)

def get_logger():
	return logging.getLogger(__name__)

@api.route("/api/<r>/<g>/<b>")
def api_set_rgb(r, g, b):
	get_logger().info("Handling /api/{}/{}/{}".format(r, g, b))
	
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