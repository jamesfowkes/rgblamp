import datetime
import logging

from alarm.lamp import Lamp
from alarm.alarm_manager import AlarmManager
import alarm.buttons as buttons
from alarm.lamp_data_provider import HTTPLampDataProvider
from alarm.alarm_data_provider import HTTPAlarmDataProvider
import simtime

lamp_data_provider = HTTPLampDataProvider("http://127.0.0.1:5000/api/")
alarm_data_provider = HTTPAlarmDataProvider("http://127.0.0.1:5000/api/")

lamp = Lamp(lamp_data_provider)

alarm_manager = AlarmManager(alarm_data_provider, 2)

def get_logger():
    return logging.getLogger(__name__)

def on_alarm_1_set(alarm_manager, lamp):
    get_logger().info("Handling alarm 1 set")
    simtime.set(alarm_manager[0].time())
    
def on_alarm_2_set(alarm_manager, lamp):
    get_logger().info("Handling alarm 2 set")
    simtime.set(alarm_manager[1].time())

class SimButtonsManager(buttons.ButtonsManager):

    BUTTON_DIAMETER = 100
    BUTTON_SPACING = 120

    def __init__(self, button_state_provider):

        buttons.ButtonsManager.__init__(self, button_state_provider)

        self.alarm_buttons = [
            buttons.Button("Alarm 1", on_alarm_1_set),
            buttons.Button("Alarm 2", on_alarm_2_set)
        ]

    def all_buttons(self):
        return self.main_buttons + self.alarm_buttons

    def get_dimensions(self):
        x = 100
        count = 0
        _limit = len(self.main_buttons)
        while count < _limit:
            yield([x, 300, self.BUTTON_DIAMETER, self.BUTTON_DIAMETER])
            x += self.BUTTON_SPACING
            count += 1

        x = 100
        count = 0
        while count < _limit:
            yield([x, 300 + self.BUTTON_SPACING, self.BUTTON_DIAMETER, self.BUTTON_DIAMETER])
            x += self.BUTTON_SPACING
            count += 1

def draw_buttons(button_manager):
    fill(255, 255, 255)
    dims = button_manager.get_dimensions()
    for button_text in button_manager.texts():
        dimension = dims.next()
        fill(255, 255, 255)
        ellipse(*dimension)
        textSize(12)
        textAlign(CENTER, CENTER)
        fill(0,0,0)
        text(button_text, dimension[0], dimension[1])
        
def draw_gui(button_manager):
    draw_buttons(button_manager)

def draw_lamp(lamp):
    fill(*lamp.get_color())
    rect(0, 0, 800, 200)
    
def draw_time(hours, minutes):
    fill(0, 0, 0)
    textAlign(CENTER, CENTER)
    textSize(32)
    text("Time: {:02}:{:02}".format(hours, minutes), 400, 220)

class SimButtonStateProvider(buttons.ButtonStateProvider):

    def __init__(self):
        buttons.ButtonStateProvider.__init__(self)
        self.button = None

    def set(self, button):
        self.button = button

    def is_pressed(self, button):
        pressed = self.button == button

        if pressed:
            self.button = None

        return pressed

button_state_provider = SimButtonStateProvider()
button_manager = SimButtonsManager(button_state_provider)

logging.basicConfig(level=logging.INFO)

def program_loop(time):
    
    state = alarm_manager.update_time(time)
    lamp.update(state)
    button_manager.update(alarm_manager, lamp)

def setup():
    size(800, 600)
    
def draw():
    background(128)
    
    time = simtime.tick()

    program_loop(time)

    draw_gui(button_manager)
    draw_lamp(lamp)
    draw_time(time.hour, time.minute)
    
def get_button_with_xy_internal(x, y):
    dims = button_manager.get_dimensions()
    
    button = None
    for i, dim in enumerate(dims):
        center_x = dim[0]
        center_y = dim[1]
        radius = dim[2] / 2
        if (x - center_x)**2 + (y - center_y)**2 < radius**2:
            button = button_manager[i]
        
    return button
        
def mouseClicked():
    get_logger().info("Mouse click!")
    button = get_button_with_xy_internal(mouseX, mouseY)
    button_state_provider.set(button)
