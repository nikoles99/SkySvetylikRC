import time
import logging
import pigpio
import RPi.GPIO as GPIO

from services.receiver_pwm_reader import ReceiverPMWReader
from services.beeper import Beeper

from constants.constants import APP_NAME


class Executor:

    def __init__(self):
        self.__default_GPIO_config()
        self.PITCH_GPIO = 3  # тангаж
        self.ROLL_GPIO = 3  # крен
        self.YAW_GPIO = 3  # рысканье
        self.GAS_GPIO = 3
        self.ESC_FORWARD_LEFT_GPIO = 4
        self.ESC_BACKWARD_LEFT_GPIO = 14
        self.ESC_BACKWARD_RIGHT_GPIO = 15
        self.ESC_FORWARD_RIGHT_GPIO = 18

        self.start = time.time()
        self.RUN_TIME = 60.0
        self.SAMPLE_TIME = 1.0
        self.board = pigpio.board()
        self.receiver_reader = ReceiverPMWReader(self.board, self.GAS_GPIO)
        self.logger = logging.getLogger(APP_NAME)
        self.logger.setLevel(logging.ERROR)
        pass

    def __default_GPIO_config(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

    def execute(self):
        try:
            Beeper.init()
            while (time.time() - self.start) < self.RUN_TIME:
                frequency = self.receiver_reader.frequency()
                pulse_width = self.receiver_reader.pulse_width()
                duty_cycle = self.receiver_reader.duty_cycle()
                self.board.set_servo_pulsewidth(self.ESC_FORWARD_LEFT_GPIO, pulse_width)
                self.board.set_servo_pulsewidth(self.ESC_BACKWARD_LEFT_GPIO, pulse_width)
                self.board.set_servo_pulsewidth(self.ESC_BACKWARD_RIGHT_GPIO, pulse_width)
                self.board.set_servo_pulsewidth(self.ESC_FORWARD_RIGHT_GPIO, pulse_width)
                print("frequency={:.1f} pulse_width={} duty_cycle={:.2f}"
                      .format(frequency, int(pulse_width + 0.5), duty_cycle))
        except Exception as exception:
            Beeper.error()
            self.logger.error(exception)
            self.receiver_reader.cancel()
            Beeper.turn_off()


executor = Executor()
executor.execute()
