class Sensor:

    def __init__(self, mock=False):
        self.mock = mock
        if not mock:
            from Adafruit_MPR121 import MPR121

            sensor = MPR121.MPR121()
            sensor.begin()

    def get_button_states(self):
        if self.mock:
            return [False, False, False, False, False, False]
        else:
            return [sensor.is_touched(i) for i in range(6)]
