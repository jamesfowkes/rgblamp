#!/usr/bin/python3
""" application.py
Usage:
    application.py <delay> <logfile>

"""

import logging
import logging.handlers
import os
import datetime
import time
import docopt

from collections import namedtuple

from multiprocessing import Process

from rgblamp.buttons.buttons import ButtonsManager
from rgblamp.alarm.alarm_manager import AlarmManager
from rgblamp.alarm.alarm_data_provider import HTTPAlarmDataProvider
from rgblamp.buttons.button_state_provider import SocketButtonStateProvider
from rgblamp.lamp.lamp import Lamp, HTTPLampController
from rgblamp.lamp.lamp_data_provider import HTTPLampDataProvider


from rgblamp.application.appapi import app

APIContext = namedtuple("APIContext", ["current_rgb"])

def get_logger():
    return logging.getLogger(__name__)

def application_task():
    while(True):
        alarm_level = alarm_manager.update_time(datetime.datetime.now())
        lamp.update(alarm_level)
        buttons_manager.update(alarm_manager, lamp)

def current_rgb():
    return (0,0,0)#lamp_controller.current_rgb()

if __name__ == "__main__":

    args = docopt.docopt(__doc__)

    #time.sleep(int(args["<delay>"]))

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    logging.basicConfig(level=logging.INFO)

    logging_handler = logging.handlers.RotatingFileHandler(args["<logfile>"], maxBytes=1024*1024, backupCount=3)
    logging_handler.setFormatter(formatter)
    get_logger().setLevel(logging.INFO)
    get_logger().addHandler(logging_handler)

    config_url = "http://0.0.0.0:" + os.getenv("RGBLAMP_CONFIG_PORT") + "/api/"
    lamp_controller_url = "http://0.0.0.0:" + os.getenv("RGBLAMP_LAMP_PORT") + "/api/"
    button_ip = "0.0.0.0"
    button_port = int(os.getenv("RGBLAMP_BUTTON_PORT"))
   
    get_logger().info("Configuration URL: {}".format(config_url))
    alarm_time_provider = HTTPAlarmDataProvider(config_url)
    lamp_data_provider = HTTPLampDataProvider(config_url)

    get_logger().info("Lamp controller URL: {}".format(lamp_controller_url))
    lamp_controller = HTTPLampController(lamp_controller_url)

    get_logger().info("Button socket IP:port: {}:{}".format(button_ip, button_port))
    button_state_provider = SocketButtonStateProvider(button_ip, button_port)

    alarm_manager = AlarmManager(alarm_time_provider, 2, logging=(logging_handler, logging.INFO))
    buttons_manager = ButtonsManager(button_state_provider, logging=(logging_handler, logging.INFO))
    lamp = Lamp(lamp_data_provider, lamp_controller, logging=(logging_handler, logging.INFO))

    get_logger().info("Waiting for alarm time provider")
    alarm_time_provider.wait_for_connection()
    get_logger().info("Waiting for lamp data provider")
    lamp_data_provider.wait_for_connection()
    get_logger().info("Waiting for button state provider")
    button_state_provider.wait_for_connection()

    lamp.flash(255, 255, 255, 10)
    time.sleep(1)

    get_logger().info("Starting application")
    application_process = Process(target=application_task)
    application_process.start()

    get_logger().info("Starting API on port {}".format(os.getenv("RGBLAMP_APPLICATION_PORT")))
    api_context = APIContext(current_rgb)
    app.config["context"] = api_context
    os.environ["PYTHONPATH"] =  os.getcwd() #Fix for import error when Werkzeug restarts (https://github.com/pallets/flask/issues/1246)
    app.run(host='0.0.0.0', port=int(os.getenv("RGBLAMP_APPLICATION_PORT")), debug=True)
