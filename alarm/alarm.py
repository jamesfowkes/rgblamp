from __future__ import division

import unittest
import datetime
import logging

ALARM_DURATION_MINUTES = 30
ALARM_DURATION_SECONDS = ALARM_DURATION_MINUTES * 60

def get_logger():
    return logging.getLogger(__name__)

def times_straddle_midnight(alarm_time, current_time):
    over_midnight = alarm_time.hour == 23
    over_midnight = over_midnight and alarm_time.minute >= (60-ALARM_DURATION_MINUTES/2)
    over_midnight = over_midnight and current_time.hour == 0
    over_midnight = over_midnight and current_time.minute <= (ALARM_DURATION_MINUTES/2)
    return over_midnight

def get_state(minutes=None, alarm_dt=None, current_datetime=None):
    if alarm_dt and current_datetime:
        seconds_since_start = (alarm_dt - current_datetime).seconds
        seconds_since_start = ALARM_DURATION_SECONDS - seconds_since_start
    else:
        seconds_since_start = minutes * 60

    return (seconds_since_start * seconds_since_start) / (ALARM_DURATION_SECONDS * ALARM_DURATION_SECONDS);

def in_alarm_period(alarm_dt, dt):
    if dt > alarm_dt:
        return False
	
    diff = alarm_dt - dt 
    return diff.seconds <= ALARM_DURATION_SECONDS

class Alarm:

    def __init__(self, alarm_time_provider, n):

        self.n = n
        self.alarm_time_provider = alarm_time_provider
        get_logger().info("Getting alarm time from {}".format(self.alarm_time_provider.url))
        self.alarm_time = self.alarm_time_provider.get_time(self.n)
        
        self.cancelled = False
        
    def cancel(self):
        self.cancelled = True
        
    def reset(self):
        self.cancelled = False

    def time(self):
        return self.alarm_time
        
    def update(self, current_datetime):
     
        state = None

        self.alarm_time = self.alarm_time_provider.get_time(self.n)
        alarm_dt = datetime.datetime.combine(datetime.date.today(), self.alarm_time)
        
        _in_alarm_period = in_alarm_period(alarm_dt, current_datetime)
        if self.cancelled and not _in_alarm_period:
            self.cancelled = False

        if not self.cancelled and _in_alarm_period:
            state = get_state(alarm_dt=alarm_dt, current_datetime=current_datetime)

        get_logger().info("Alarm %d state: %s in alarm period, (%s cancelled)", self.n,  "" if _in_alarm_period else "not", "" if self.cancelled else "not")
        return state

class MockAlarmDataProvider:

    def __init__(self, time):
        self.time = time

    def url(self):
        return "mock"

    def get_time(self, n):
        return self.time

class AlarmTests(unittest.TestCase):

    def get_test_datetime(self, hh, mm, plus_days=0):
        test_datetime = datetime.datetime.combine(datetime.date.today(), datetime.time(hour=hh, minute=mm))
        test_datetime += datetime.timedelta(days=plus_days)

        return test_datetime

    def test_alarmIsOffOneMinuteBeforeAlarmTime(self):
        alarm = Alarm(MockAlarmDataProvider(datetime.time(7, 30)), 0)
        state = alarm.update(self.get_test_datetime(6, 59))
        self.assertEqual(None, state)

    def test_alarmIsOffOneMinuteAfterAlarmDuration(self):
        alarm = Alarm(MockAlarmDataProvider(datetime.time(7, 30)), 0)
        state = alarm.update(self.get_test_datetime(9, 1))
        self.assertEqual(None, state)

    def test_alarmIsInCorrectStateTenMinutesBeforeTime(self):
        alarm = Alarm(MockAlarmDataProvider(datetime.time(7, 30)), 0)
        state = alarm.update(self.get_test_datetime(7, 20))
        state = alarm.update(self.get_test_datetime(7, 20))
        self.assertAlmostEqual(get_state(20), state)

    def test_alarmIsInCorrectStateFifteenMinutesBeforeTime(self):
        alarm = Alarm(MockAlarmDataProvider(datetime.time(7, 30)), 0)
        state = alarm.update(self.get_test_datetime(7, 15))
        self.assertAlmostEqual(get_state(15), state)

    def test_alarmIsInCorrectStateTwentyTwoMinutesBeforeTime(self):
        alarm = Alarm(MockAlarmDataProvider(datetime.time(7, 30)), 0)
        state = alarm.update(self.get_test_datetime(7, 8))
        self.assertAlmostEqual(get_state(8), state)

    def test_alarmIsOffAtEndOfDuration(self):
        alarm = Alarm(MockAlarmDataProvider(datetime.time(7, 30)), 0)
        state = alarm.update(self.get_test_datetime(9, 0))
        self.assertEqual(None, state)

    def test_alarmHandlesCrossingMidnight(self):

        mock = MockAlarmDataProvider(datetime.time(00, 15))
        alarm = Alarm(mock, 0)
        
        state = alarm.update(self.get_test_datetime(23, 44, plus_days=-1))
        self.assertEqual(None, state)
        
        state = alarm.update(self.get_test_datetime(23, 45, plus_days=-1))
        self.assertEqual(0, state)
        
        state = alarm.update(self.get_test_datetime(0, 0))
        self.assertEqual(get_state(15), state)
        
        t1 = self.get_test_datetime(0, 15)
        t2 = datetime.datetime.combine(datetime.date.today(), mock.get_time(0))
        
        state = alarm.update(self.get_test_datetime(0, 15))
        self.assertEqual(1, state)
        
        state = alarm.update(self.get_test_datetime(0, 16))
        self.assertEqual(None, state)
        
    def test_alarmCanBeCancelledAfterActivation(self):
        alarm = Alarm(MockAlarmDataProvider(datetime.time(7, 30)), 0)
        state = alarm.update(self.get_test_datetime(7, 15))
        self.assertAlmostEqual(get_state(15), state)
        alarm.cancel()
        state = alarm.update(self.get_test_datetime(7, 15))
        self.assertEqual(None, state)
    
    def test_alarmIsReactivatedAfterCancellation(self):
        alarm = Alarm(MockAlarmDataProvider(datetime.time(7, 30)), 0)
        state = alarm.update(self.get_test_datetime(7, 15))
        alarm.cancel()
        state = alarm.update(self.get_test_datetime(7, 31))
        state = alarm.update(self.get_test_datetime(7, 0))
        self.assertEqual(0, state)


if __name__ == "__main__":
    unittest.main()