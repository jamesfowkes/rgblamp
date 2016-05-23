import logging
from collections import namedtuple

Button = namedtuple('Button', ['text', 'handler'])

def get_logger():
    return logging.getLogger(__name__)

def on_onoff_button(alarm_manager, lamp):

    get_logger().info("Handling on/off")
    
    if lamp.get_brightness() > 0:
        lamp.set_mode(lamp.MODE_OFF)
    else:
        lamp.set_mode(lamp.MODE_ON)

    get_logger().info("Onoff: New colour: %s", lamp.get_color())

def on_bright_button(alarm_manager, lamp):
    get_logger().info("Handling bright button")
    lamp.increase_brightness()

def on_dim_button(alarm_manager, lamp):
    get_logger().info("Handling dim button")
    lamp.decrease_brightness()

def on_cycle_button(alarm_manager, lamp):
    get_logger().info("Handling cycle button")
    lamp.set_mode(lamp.MODE_CYCLE)

def on_snooze_button(alarm_manager, lamp):
    get_logger().info("Handling snooze button")

def on_alarm_change(alarm_manager, lamp):
    get_logger().info("Handling alarm change")
    alarm_manager.set_next()
    
def on_alarm_cancel(alarm_manager, lamp):
    get_logger().info("Handling alarm cancel")
    alarm_manager.cancel()

BUTTONS = [
    Button("Change Alarm", on_alarm_change),
    Button("Light On/Off", on_onoff_button),
    Button("Bright", on_bright_button),
    Button("Dim", on_dim_button),
    Button("Colour Change", on_cycle_button),
    Button("Snooze", on_snooze_button)
]

class ButtonStateProvider:

    def __init__(self):
        pass

    def get_pressed(self):
        raise Exception("Must be overridden by superclass")

class ButtonsManager:

    def __init__(self, button_state_provider):

        self.main_buttons = BUTTONS

        self.button_state_provider = button_state_provider

        self.cancel_alarm_callback = on_alarm_cancel
       
    def __getitem__(self, key):
        return self.all_buttons()[key]

    def all_buttons(self):
        return self.main_buttons

    def texts(self):
        return [b.text for b in self.all_buttons()]

    def update(self, alarm_manager, lamp):

        for button in self.all_buttons():
            if self.button_state_provider.is_pressed(button):
                self.handle_button_press(button, alarm_manager, lamp)

    def handle_button_press(self, button, alarm_manager, lamp):
        
        if button in self.main_buttons:
            self.cancel_alarm_callback(alarm_manager, lamp)

        get_logger().info("Handling button '%s'", button.text)
        button.handler(alarm_manager, lamp)
        