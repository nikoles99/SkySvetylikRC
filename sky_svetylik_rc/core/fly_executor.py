import subprocess

from constants.constants import GAS_MIN, YAW_MAX, ERROR_MS
from core.executor import Executor
from exceptions.no_receiver_connection_exception import NoReceiverConnectionException
from services.beeper import Beeper


class FlyExecutor(Executor):

    def __init__(self):
        super().__init__()
        self.MIN_START_ROTATE_PW = 150

    def execute(self):
        try:
            self.drone.gas(GAS_MIN, GAS_MIN, GAS_MIN, GAS_MIN)
            self.arm()
            while True:
                if self.is_stick_bottom_left():
                    self.drone.gas(GAS_MIN, GAS_MIN, GAS_MIN, GAS_MIN)
                    self.arm()
                self.drone.update(self.transmitter)
        except Exception as exception:
            self.drone.gas(GAS_MIN, GAS_MIN, GAS_MIN, GAS_MIN)
            Beeper().error()
            self.logger.error(exception)

    def arm(self):
        Beeper().init()
        self.logger.info('START')
        while True:
            if self.transmitter.gas_pw == 0 or self.transmitter.yaw_pw == 0 or self.transmitter.pitch_pw == 0 or self.transmitter.roll_pw == 0:
                raise NoReceiverConnectionException()
            if self.is_stick_bottom_left():
                Beeper().start()
                break

    def is_stick_bottom_left(self):
        return self.transmitter.gas_pw - GAS_MIN <= ERROR_MS and YAW_MAX - self.transmitter.yaw_pw <= ERROR_MS

    def turn_off(self):
        Beeper().turn_off()
        subprocess.Popen('sudo shutdown now', stdout=subprocess.PIPE, shell=True).communicate()
