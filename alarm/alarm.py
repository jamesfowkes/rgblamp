from __future__ import division

import unittest
import datetime
import logging

def get_logger():
    return logging.getLogger(__name__)

def times_straddle_midnight(alarm_time, current_time):
    return alarm_time.hour == 23 and alarm_time.minute >= 45 and current_time.hour == 0 and current_time.minute <=15
    
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
        alarm_datetime = datetime.datetime.combine(datetime.date.today(), self.alarm_time)
        diff = current_datetime - alarm_datetime
        diff_minutes = diff.seconds / 60

        in_alarm_period = diff_minutes <= 30

        if self.cancelled and not in_alarm_period:
            self.cancelled = False

        if not self.cancelled and in_alarm_period:
            state = diff_minutes / 30
            state = state * state

        get_logger().info("Alarm %d state: %s in alarm period, (%s cancelled)", self.n,  "" if in_alarm_period else "not", "" if self.cancelled else "not")
        return state

class MockAlarmDataProvider:

    def __init__(self, time):
        self.time = time

    def get_time(self, n):
        return self.time

class AlarmTests(unittest.TestCase):

    def get_test_datetime(self, hh, mm, plus_days=0):
        test_datetime = datetime.datetime.combine(datetime.date.today(), datetime.time(hour=hh, minute=mm))
        test_datetime += datetime.timedelta(days=plus_days)

        return test_datetime

    def test_alarmIsOffOneMinuteBeforeAlarmTime(self):
        alarm = Alarm(MockAlarmDataProvider(datetime.time(7, 30)), 0)
        state = alarm.update(self.get_test_datetime(7, 29))
        self.assertEqual(None, state)

    def test_alarmIsOffOneMinuteAfterAlarmDuration(self):
        alarm = Alarm(MockAlarmDataProvider(datetime.time(7, 30)), 0)
        state = alarm.update(self.get_test_datetime(9, 1))
        self.assertEqual(None, state)

    def test_alarmIsOnThirdOnTenMinutesAfterTime(self):
        alarm = Alarm(MockAlarmDataProvider(datetime.time(7, 30)), 0)
        state = alarm.update(self.get_test_datetime(7, 40))
        self.assertAlmostEqual(1 / 3, state)

    def test_alarmIsHalfOnFifteenMinutesAfterTime(self):
        alarm = Alarm(MockAlarmDataProvider(datetime.time(7, 30)), 0)
        state = alarm.update(self.get_test_datetime(7, 45))
        self.assertAlmostEqual(0.5, state)

    def test_alarmIsOffAtEndOfDuration(self):
        alarm = Alarm(MockAlarmDataProvider(datetime.time(7, 30)), 0)
        state = alarm.update(self.get_test_datetime(9, 0))
        self.assertEqual(None, state)

    def test_alarmHandlesCrossingMidnight(self):
        alarm = Alarm(MockAlarmDataProvider(datetime.time(23, 45)), 0)
        
        state = alarm.update(self.get_test_datetime(23,44))
        self.assertEqual(None, state)
        
        state = alarm.update(self.get_test_datetime(23,45))
        self.assertEqual(0, state)
        
        state = alarm.update(self.get_test_datetime(0,0))
        self.assertEqual(1/2, state)
        
        state = alarm.update(self.get_test_datetime(0,15))
        self.assertEqual(1, state)
        
        state = alarm.update(self.get_test_datetime(0,16))
        self.assertEqual(None, state)
        
    def test_alarmCanBeCancelledAfterActivation(self):
        alarm = Alarm(MockAlarmDataProvider(datetime.time(7, 30)), 0)
        state = alarm.update(self.get_test_datetime(7, 45))
        self.assertAlmostEqual(0.5, state)
        alarm.cancel()
        state = alarm.update(self.get_test_datetime(7, 45))
        self.assertEqual(None, state)
    
    def test_alarmIsReactivatedAfterCancellation(self):
        alarm = Alarm(MockAlarmDataProvider(datetime.time(7, 30)), 0)
        state = alarm.update(self.get_test_datetime(7, 45))
        alarm.cancel()
        state = alarm.update(self.get_test_datetime(8, 1))
        state = alarm.update(self.get_test_datetime(7, 30))
        self.assertEqual(0, state)


if __name__ == "__main__":
    unittest.main()