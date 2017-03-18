import logging
import serial
import json
import time

from flask import Blueprint, jsonify, current_app, request

api = Blueprint('api', __name__)

def get_logger():
	return logging.getLogger(__name__)

def setup_logger(handler):
    get_logger().setLevel(logging.INFO)
    get_logger().addHandler(handler)

@api.route("/api/rgb")
def get_rgb():
	return jsonify({"endpoint":request.path, "rgb":current_app.config["context"].current_rgb()})