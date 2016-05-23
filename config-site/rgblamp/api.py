import logging
import json
import datetime

from flask import Blueprint, request, Response

from rgblamp.persistent_config import PersistentConfig

def get_logger():
	return logging.getLogger(__name__)

api = Blueprint('api', __name__)

config = PersistentConfig("rgblamp.cfg")

def rgb_string_to_tuple(rgb):
	rgb = rgb.split(",")
	rgb = [int(bit.strip()) for bit in rgb]
	return (rgb[0], rgb[1], rgb[2])

@api.route("/api/lamp/rgb/normal")
def api_get_rgb_normal():
	get_logger().info("Handling /api/lamp/rgb/normal")

	return json.dumps(
		{
			"req":"/api/lamp/rgb/normal",
			"rgb": rgb_string_to_tuple(config.rgb_normal)
		}
	)

@api.route("/api/lamp/rgb/alarm")
def api_get_rgb_alarm():
	get_logger().info("Handling /api/lamp/rgb/alarm")

	return json.dumps(
		{
			"req":"/api/lamp/rgb/alarm",
			"rgb": rgb_string_to_tuple(config.rgb_alarm)
		}
	)

@api.route("/api/lamp/brightness/normal")
def api_get_normal_brightness():
	get_logger().info("Handling /api/lamp/brightness/normal")
	brightness = config.default_brightness

	return json.dumps(
		{
			"req":"/api/lamp/brightness/normal",
			"brightness": brightness
		}
	)

@api.route("/api/lamp/brightness/alarm")
def api_get_alarm_brightness():
	get_logger().info("Handling /api/lamp/brightness/alarm")
	brightness = config.default_brightness

	return json.dumps(
		{
			"req":"/api/lamp/brightness/alarm",
			"brightness": brightness
		}
	)

@api.route("/api/alarm/<num>/time")
def api_get_alarm_1(num):
	req = "/api/alarm/%s/time" % num
	get_logger().info("Handling %s", req)
	alarm_time = config.get("alarm%s_time" % num)
	alarm_time = alarm_time.strftime("%H:%M")
	get_logger().info("Returning %s", alarm_time)
	return json.dumps(
		{
			"req": req,
			"time": alarm_time
		}
	)

@api.route("/api/clear/<item>")
def api_clear_item(item):
	get_logger().info("Handling /api/clear/{}".format(item))
	config.set(**{item: None})
	return json.dumps(
		{
			"req":"/api/clear/{}".format(item),
			"success": True
		}
	)
