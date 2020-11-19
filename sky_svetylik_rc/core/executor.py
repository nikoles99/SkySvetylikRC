import abc
import pigpio
import logging

from constants.constants import APP_NAME
from services.receiver_pwm_reader import ReceiverPMWReader
from core.sky_svetulic_rc import SkySvetylicRC
from utils.config_utils import ConfigUtils


class Executor:

    def __init__(self):
        self.board = pigpio.pi()
        self.drone = SkySvetylicRC(self.board)
        self.receiver_left_vertical = ReceiverPMWReader(self.board, ConfigUtils.read_value('pinIn.reciever.leftVercical'))
        self.receiver_left_horizontal = ReceiverPMWReader(self.board, ConfigUtils.read_value('pinIn.reciever.leftHorizontal'))
        self.receiver_right_vertical = ReceiverPMWReader(self.board, ConfigUtils.read_value('pinIn.reciever.rightVertical'))
        self.receiver_right_horizontal = ReceiverPMWReader(self.board, ConfigUtils.read_value('pinIn.reciever.rightHorizontal'))
        self.logger = logging.getLogger(APP_NAME)
        pass

    @abc.abstractmethod
    def execute(self):
        pass
