import datetime
import logging
import os

from collections import namedtuple
from itertools import tee

from transitions import Machine

from rgblamp.alarm.alarm import Alarm

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def get_logger():
    return logging.getLogger(__name__)

def alarm_state_str_to_index(alarm_string):
    
    alarm_number = None
    if alarm_string.startswith("alarm"):
        alarm_number = int(alarm_string[5:]) - 1
        
    return alarm_number

def get_state_strings(state_count):
    states =  ["alarm%d" % (i+1) for i in range(state_count)]
    states.insert(0, "no_alarm")
    return states

class AlarmManager:

    def add_state_transitions(self, states):

        count = len(states)
        if count == 0:
            return

        for old, new in pairwise(states): 
            self.machine.add_transition('next_alarm', old, new)

        self.machine.add_transition('next_alarm', new, 'no_alarm')


    def __init__(self, alarm_time_provider, alarm_count, logging, time=datetime.datetime.now()):

        get_logger().addHandler(logging[0])
        get_logger().setLevel(logging[1])

        states = get_state_strings(alarm_count)

        self.machine = Machine(model=self, states=states, initial="no_alarm", after_state_change='reset_current_alarm')
        
        self.alarms = [Alarm(alarm_time_provider, n+1) for n in range(alarm_count)]
        
        self.add_state_transitions(states)

        self.last_update = time

    def reset_current_alarm(self):
        if self.current_alarm:
            self.current_alarm.reset()
               
    def update_required(self, time):
        diff = self.last_update - time
        return diff.seconds > 2 

    def __getitem__(self, key):
        return self.alarms[key]

    @property
    def current_alarm(self):
        
        alarm_number = alarm_state_str_to_index(self.state)
        alarm = self.alarms[alarm_number] if alarm_number is not None else None
        return alarm
    
    def update_time(self, time):

        alarm_state = None

        if self.update_required(time):
            self.last_update = time           

            alarm = self.current_alarm
            alarm_state = alarm.update(time) if alarm is not None else None

        return alarm_state

    def set_next(self):
        self.next_alarm()

    def cancel(self):
        for alarm in self.alarms:
            alarm.cancel()
