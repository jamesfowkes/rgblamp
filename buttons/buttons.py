import logging
import datetime

from collections import namedtuple

Button = namedtuple('Button', ['text', 'handler', 'number'])

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
    if alarm_manager.current_alarm is None:
        lamp.flash(16, 0, 0, 1)
    elif alarm_manager.current_alarm.n == 1:
        lamp.flash(0, 16, 0, 1)
    elif alarm_manager.current_alarm.n == 2:
        lamp.flash(0, 0, 16, 1)

def on_alarm_cancel(alarm_manager, lamp):
    get_logger().info("Handling alarm cancel")
    alarm_manager.cancel()

BUTTONS = [
    Button("Change Alarm", on_alarm_change, 0),
    Button("Light On/Off", on_onoff_button, 1),
    Button("Bright", on_bright_button, 2),
    Button("Dim", on_dim_button, 3),
    Button("Colour Change", on_cycle_button, 4),
    Button("Snooze", on_snooze_button, 5)
]

class ButtonsManager:

    def __init__(self, button_state_provider, logging):

        get_logger().addHandler(logging[0])
        get_logger().setLevel(logging[1])

        self.main_buttons = BUTTONS

        self.button_state_provider = button_state_provider

        self.cancel_alarm_callback = on_alarm_cancel

        self.last_press = datetime.datetime.now()    
    
    def __getitem__(self, key):
        return self.all_buttons()[key]

    def all_buttons(self):
        return self.main_buttons

    def texts(self):
        return [b.text for b in self.all_buttons()]

    def update(self, alarm_manager, lamp):

        if (datetime.datetime.now() - self.last_press).microseconds > 500000:
            button_states = self.button_state_provider.get_state()
            for button in self.all_buttons():
                if button_states[button.number]:
                    self.last_press = datetime.datetime.now()
                    self.handle_button_press(button, alarm_manager, lamp)

    def handle_button_press(self, button, alarm_manager, lamp):
        
        if button in self.main_buttons:
            self.cancel_alarm_callback(alarm_manager, lamp)

        get_logger().info("Handling button '%s'", button.text)
        button.handler(alarm_manager, lamp)
        
