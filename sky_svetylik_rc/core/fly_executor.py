import subprocess

from core.executor import Executor
from exceptions.no_receiver_connection_exception import NoReceiverConnectionException
from services.beeper import Beeper
from utils.config_utils import ConfigUtils


class FlyExecutor(Executor):

    def __init__(self):
        super().__init__()
        self.l_v_min = ConfigUtils.read_value('calibration.leftVertical.min')
        self.l_h_max = ConfigUtils.read_value('calibration.leftHorizontal.max')
        self.r_v_min = ConfigUtils.read_value('calibration.rightVertical.min')
        self.r_h_min = ConfigUtils.read_value('calibration.rightHorizontal.min')
        self.error_ms = 10

    def execute(self):
        try:
            self.arm()
            while True:
                if self.is_disarmed():
                    raise NoReceiverConnectionException()
                self.drone.update(self.transmitter)
        except Exception as exception:
            self.logger.error(exception)
        finally:
            self.drone.gas(self.l_v_min, self.l_v_min, self.l_v_min, self.l_v_min)
            Beeper().error()

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
        return self.transmitter.gas_pw - self.l_v_min <= self.error_ms and self.transmitter.yaw_pw - self.l_h_max <= self.error_ms \
               and self.transmitter.pitch_pw - self.r_v_min <= self.error_ms and self.transmitter.roll_pw - self.r_h_min <= self.error_ms

    @staticmethod
    def turn_off():
        Beeper().turn_off()
        subprocess.Popen('sudo shutdown now', stdout=subprocess.PIPE, shell=True).communicate()
