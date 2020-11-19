import time

from core.executor import Executor
from domain.stick_range import StickRange
from services.beeper import Beeper
from utils.config_utils import ConfigUtils


class TransmitterCalibrationExecutor(Executor):

    def __init__(self):
        super().__init__()
        self.start = time.time()
        self.RUN_TIME = 10.0
        self.r_h_stick = StickRange()
        self.r_v_stick = StickRange()
        self.l_h_stick = StickRange()
        self.l_v_stick = StickRange()

    def execute(self):
        try:
            Beeper().init()
            self.logger.info('START CALIBRATION')
            while (time.time() - self.start) < self.RUN_TIME:
                self.__update_pulse_width(self.r_h_stick, self.transmitter.roll_pulse_width)
                self.__update_pulse_width(self.r_v_stick, self.transmitter.pitch_pulse_width)
                self.__update_pulse_width(self.l_h_stick, self.transmitter.yaw_pulse_width)
                self.__update_pulse_width(self.l_v_stick, self.transmitter.gas_pulse_width)
        except Exception as exception:
            self.logger.error(exception)
        finally:
            self.__update_calibrated_values('calibration.rightHorizontal.min', 'calibration.rightHorizontal.max', self.r_h_stick)
            self.__update_calibrated_values('calibration.rightVertical.min', 'calibration.rightVertical.max', self.r_v_stick)
            self.__update_calibrated_values('calibration.leftHorizontal.min', 'calibration.leftHorizontal.max', self.l_h_stick)
            self.__update_calibrated_values('calibration.leftVertical.min', 'calibration.leftVertical.max', self.l_v_stick)
            self.logger.info('FINISH CALIBRATION')
            Beeper().finish()

    @staticmethod
    def __update_pulse_width(stick, pulse_width):
        if stick.min is None or pulse_width < stick.min:
            stick.min = pulse_width
        if stick.max is None or pulse_width > stick.max:
            stick.max = pulse_width

    @staticmethod
    def __update_calibrated_values(min_key, max_key, stick):
        ConfigUtils.write_value(min_key, stick.min)
        ConfigUtils.write_value(max_key, stick.max)
