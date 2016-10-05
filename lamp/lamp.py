import datetime
import logging
import requests
import random

def get_logger():
    return logging.getLogger(__name__)

def get_random_change(_min, _max):
    change = random.randint(_min, _max)
    if change > 0 and change < 1:
        change = 1

    if change < 0 and change > -1:
        change = -1

    return change

class HTTPLampController:

    def __init__(self, url):
        self.url = url

    def set_rgb(self, r, g, b):
        get_logger().info("Requesting RGB values %d, %d, %d", r, g, b)
        resp = requests.get(self.url + "{}/{}/{}".format(r, g, b))
        
class TimedFunction:

    def __init__(self, fn, **kwargs):
        self.fn = fn
        self.last_time = datetime.datetime.now()
        self.kwargs = kwargs

    def time_expired(self):
        expired = False
        if "seconds" in self.kwargs:
            expired = (datetime.datetime.now() - self.last_time).seconds > self.kwargs["seconds"] 
        elif "microseconds" in self.kwargs:
            expired = (datetime.datetime.now() - self.last_time).microseconds > self.kwargs["microseconds"]

        return expired

    def tick(self):
        if self.time_expired():
            self.last_time = datetime.datetime.now()
            self.fn()

class Lamp:
    MODE_ON = 0
    MODE_OFF = 1
    MODE_CYCLE = 2
    MODE_ALARM = 3
    
    MODE_STRINGS = ["On", "Off", "Cycle", "Alarm"]
    
    def __init__(self, lamp_data_provider, lamp_controller):
        self.lamp_data_provider = lamp_data_provider
        self.lamp_controller = lamp_controller
        self.current_brightness = 0
        self.current_color = [0, 0, 0]
        self.mode = self.MODE_OFF
        self.colour_cycler = TimedFunction(self.cycle_colour, microseconds=500000)
        self.colour_index_cycler = TimedFunction(self.change_cycle_index, seconds=15)

        self.cycle_index = random.randint(0, 2)

        self.update_controller()

    def set_brightness_from_alarm_state(self, alarm_state):

        new_brightness = self.lamp_data_provider.get_alarm_brightness(alarm_state)
        get_logger().info("Setting brightness %d from state %d", new_brightness, alarm_state)

        if self.current_brightness <= new_brightness:
            self.set_brightness(new_brightness)
     
    def set_colour_on_alarm_state(self, alarm_state):
        new_colour = self.lamp_data_provider.get_alarm_color(alarm_state)
        self.set_color(new_colour)
        
    def update(self, alarm_level):

        if alarm_level is not None:
            self.last_alarm_state = alarm_level
            self.set_mode(self.MODE_ALARM)
        else:
            if self.mode == self.MODE_CYCLE:
                self.colour_cycler.tick()
                self.colour_index_cycler.tick()

    def valid_mode_change(self, old_mode, new_mode):
        invalid = (old_mode == self.MODE_OFF) and (new_mode not in [self.MODE_ON, self.MODE_ALARM])
        return not invalid

    def on_mode_on(self):
        self.set_brightness()
        self.set_color()
        
    def on_mode_off(self):
        self.set_brightness(0.0)
    
    def on_mode_cycle(self):
        self.set_brightness()
        self.set_color()
        
    def on_mode_alarm(self):
        self.set_brightness_from_alarm_state(self.last_alarm_state)
        self.set_colour_on_alarm_state(self.last_alarm_state)

    def change_mode(self, new_mode):
        get_logger().info("Setting mode " + self.MODE_STRINGS[new_mode])

        self.mode = new_mode

        mode_to_function_map = {
            self.MODE_ALARM: self.on_mode_alarm,
            self.MODE_ON: self.on_mode_on,
            self.MODE_OFF: self.on_mode_off,
            self.MODE_CYCLE: self.on_mode_cycle
        }

        mode_to_function_map[new_mode]()
            
    def set_mode(self, new_mode):

        if self.valid_mode_change(self.mode, new_mode):
            self.change_mode(new_mode)
        else:
            get_logger().info("Invalid mode change: " + self.MODE_STRINGS[new_mode] + " from " + self.MODE_STRINGS[self.mode])
                        
    def set_brightness(self, new_brightness=None):
        if new_brightness is None:
            new_brightness = self.lamp_data_provider.get_normal_brightness()
        self.current_brightness = new_brightness
        get_logger().info("New brightness: {}".format(self.current_brightness))
        
        self.update_controller()

    def get_brightness(self):
        return self.current_brightness

    def set_color(self, rgb=None):
        if rgb is None:
            rgb = self.lamp_data_provider.get_normal_rgb()

        self.current_color = rgb[:]
        get_logger().info("New colour: {}, {}, {}".format(*self.current_color))

        self.update_controller()
        
    def change_cycle_index(self):
        self.cycle_index = random.randint(0, 2)

    def cycle_colour(self):
        new_color = self.current_color
        new_color[self.cycle_index] += get_random_change(-10, 10)
        new_color[self.cycle_index] = min(new_color[self.cycle_index], 255)
        new_color[self.cycle_index] = max(new_color[self.cycle_index], 0)

        self.set_color(new_color)

    def get_color(self):
        _brightness = self.get_brightness()
        return [int(c * _brightness) for c in self.current_color]

    def increase_brightness(self):
        if self.current_brightness < 1 and self.mode != self.MODE_OFF:
            self.current_brightness += 0.01
        else:
            get_logger().info("Lamp off, brightness not changed")
    
    def decrease_brightness(self):
        if self.current_brightness > 0 and self.mode != self.MODE_OFF:
            self.current_brightness -= 0.01
        else:
            get_logger().info("Lamp off, brightness not changed")

    def update_controller(self):
        r, g, b = self.get_color()
        self.lamp_controller.set_rgb(r, g, b)
