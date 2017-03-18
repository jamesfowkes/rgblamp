import requests

import logging
import time

def get_logger():
    return logging.getLogger(__name__)

class HTTPLampDataProvider:

    def __init__(self, url):
        self.url = url

    def wait_for_connection(self):
        while(True):
            try:
                resp = self.get_normal_brightness()
                return
            except requests.exceptions.ConnectionError:
                time.sleep(1)

    def get_normal_brightness(self):
        resp = requests.get(self.url + "lamp/brightness/normal")
        brightness = resp.json()['brightness']
        get_logger().info("Got normal brightness: %d%%", brightness)
        return brightness / 100

    def get_alarm_brightness(self, alarm_state):
        resp = requests.get(self.url + "lamp/brightness/alarm")
        brightness = resp.json()['brightness']
        get_logger().info("Got alarm brightness: %d%%", brightness)
        return brightness * alarm_state / 100

    def get_normal_rgb(self):
        resp = requests.get(self.url + "lamp/rgb/normal")
        rgb = resp.json()['rgb']
        get_logger().info("Got normal rgb value: %d, %d, %d", *rgb)
        return rgb

    def get_alarm_rgb(self):
        resp = requests.get(self.url + "lamp/rgb/alarm")
        rgb = resp.json()['rgb']
        get_logger().info("Got alarm rgb value: %d, %d, %d", *rgb)
        return rgb
