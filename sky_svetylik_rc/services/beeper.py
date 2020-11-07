import RPi.GPIO as GPIO

from time import sleep

from utils.config_utils import ConfigUtils


class Beeper:

    def __init__(self):
        self.buzzer = ConfigUtils.readValue('pinOut.beeper')
        GPIO.setup(self.buzzer, GPIO.OUT)
        pass

    def init(self):
        self.__beep(0.5, 3)

    def error(self):
        self.__beep(1.5, 3)

    def turn_off(self):
        self.__beep(0.5, 6)

    def __beep(self, delay_seconds=0.5, count=1):
        for i in range(0, count):
            GPIO.output(self.buzzer, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(self.buzzer, GPIO.LOW)
            sleep(delay_seconds)
