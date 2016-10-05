import logging
import os
import datetime

from rgblamp.buttons.buttons import ButtonsManager
from rgblamp.alarm.alarm_manager import AlarmManager
from rgblamp.alarm.alarm_data_provider import HTTPAlarmDataProvider
from rgblamp.buttons.button_state_provider import SocketButtonStateProvider
from rgblamp.lamp.lamp import Lamp, HTTPLampController
from rgblamp.lamp.lamp_data_provider import HTTPLampDataProvider

def get_logger():
    return logging.getLogger(__name__)

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    
    config_url = "http://0.0.0.0:" + os.getenv("RGBLAMP_CONFIG_PORT") + "/api/"
    lamp_controller_url = "http://0.0.0.0:" + os.getenv("RGBLAMP_LAMP_PORT") + "/api/"
    button_ip = "0.0.0.0"
    button_port = int(os.getenv("RGBLAMP_BUTTON_PORT"))
    
    get_logger().info("Configuration URL: {}".format(config_url))
    alarm_time_provider = HTTPAlarmDataProvider(config_url)
    lamp_data_provider = HTTPLampDataProvider(config_url)

    lamp_controller = HTTPLampController(lamp_controller_url)

    get_logger().info("Button socket IP:port: {}:{}".format(button_ip, button_port))
    button_state_provider = SocketButtonStateProvider(button_ip, button_port)

    alarm_manager = AlarmManager(alarm_time_provider, 2)
    buttons_manager = ButtonsManager(button_state_provider)
    lamp = Lamp(lamp_data_provider, lamp_controller)

    while(True):
        alarm_level = alarm_manager.update_time(datetime.datetime.now())
        lamp.update(alarm_level)
        buttons_manager.update(alarm_manager, lamp)