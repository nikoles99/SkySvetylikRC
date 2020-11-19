import subprocess

from constants.constants import GAS_MIN, PITCH_MIN, ROLL_MIN, YAW_MAX, ERROR_MS
from core.executor import Executor
from exceptions.no_receiver_connection_exception import NoReceiverConnectionException
from services.beeper import Beeper


class FlyExecutor(Executor):

    def __init__(self):
        super().__init__()

    def execute(self):
        try:
            self.arm()
            while True:
                if self.is_disarmed():
                    raise NoReceiverConnectionException()
                self.drone.update(self.transmitter)
        except Exception as exception:
            self.drone.gas(GAS_MIN, GAS_MIN, GAS_MIN, GAS_MIN)
            Beeper().error()
            self.logger.error(exception)
            #self.turn_off()

    def arm(self):
        Beeper().init()
        self.logger.info('START')
        while True:
            if self.transmitter.gas_pw == 0 or self.transmitter.yaw_pw == 0 or self.transmitter.pitch_pw == 0 or self.transmitter.roll_pw == 0:
                raise NoReceiverConnectionException()
            if self.is_disarmed():
                Beeper().start()
                break

    def is_disarmed(self):
        return self.transmitter.gas_pw - GAS_MIN <= ERROR_MS and self.transmitter.yaw_pw - YAW_MAX <= ERROR_MS \
               and self.transmitter.pitch_pw - PITCH_MIN <= ERROR_MS and self.transmitter.roll_pw - ROLL_MIN <= ERROR_MS

    def turn_off(self):
        Beeper().turn_off()
        subprocess.Popen('sudo shutdown now', stdout=subprocess.PIPE, shell=True).communicate()
