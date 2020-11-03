import RPi.GPIO as GPIO
from time import sleep


class Beeper:

    def __init__(self):
        self.buzzer = 23
        GPIO.setup(self.buzzer, GPIO.OUT)
        pass

    @staticmethod
    def init(self):
        self.__beep(0.5, 3)

    @staticmethod
    def error(self):
        self.__beep(1.5, 3)

    @staticmethod
    def turn_off(self):
        self.__beep(0.5, 6)

    def __beep(self, delay_seconds=0.5, count=1):
        for i in range(0, count):
            GPIO.output(self.buzzer, GPIO.HIGH)
            sleep(delay_seconds)
            GPIO.output(self.buzzer, GPIO.LOW)
