import abc
import logging

import pigpio

from core.sky_svetulic_rc import SkySvetylicRC
from domain.transmitter import Transmitter


class Executor:

    def __init__(self):
        self.board = pigpio.pi()
        self.drone = SkySvetylicRC(self.board)
        self.transmitter = Transmitter(self.board)
        self.logger = logging.getLogger('Executor')
        pass

    @abc.abstractmethod
    def execute(self):
        pass
