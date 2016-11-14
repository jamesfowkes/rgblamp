class Sensor:

    def __init__(self, mock=False):
        self.mock = mock
        if not mock:
            from Adafruit_MPR121 import MPR121

            self.sensor = MPR121.MPR121()
            self.sensor.begin()

    def get_button_states(self):
        if self.mock:
            return [False, False, False, False, False, False]
        else:
            return [self.sensor.is_touched(i) for i in range(6)]
