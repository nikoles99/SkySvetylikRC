import time
import logging
import pigpio
import RPi.GPIO as GPIO

from services.receiver_pwm_reader import ReceiverPMWReader
from services.beeper import Beeper

from constants.constants import APP_NAME


class Executor:

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.start = time.time()
        self.PWM_GPIO = 3
        self.RUN_TIME = 60.0
        self.SAMPLE_TIME = 1.0
        self.board = pigpio.board()
        self.receiverReader = ReceiverPMWReader(self.board, self.PWM_GPIO)
        self.logger = logging.getLogger(APP_NAME)
        self.logger.setLevel(logging.ERROR)
        pass

    def execute(self):
        try:
            Beeper.init()
            while (time.time() - self.start) < self.RUN_TIME:
                f = self.receiverReader.frequency()
                pw = self.receiverReader.pulse_width()
                dc = self.receiverReader.duty_cycle()
                self.board.set_servo_pulsewidth(4, pw)
                self.board.set_servo_pulsewidth(14, pw)
                self.board.set_servo_pulsewidth(15, pw)
                self.board.set_servo_pulsewidth(18, pw)
                print("f={:.1f} pw={} dc={:.2f}".format(f, int(pw + 0.5), dc))
        except Exception as exception:
            Beeper.error()
            self.logger.error(exception)
            self.receiverReader.cancel()
            Beeper.turn_off()


executor = Executor()
executor.execute()
