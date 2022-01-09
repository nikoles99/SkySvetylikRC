from core.sky_svetulic_rc import SkySvetylicRC
from domain.transmitter import Transmitter


class Executor:

    def __init__(self):
        self.drone = SkySvetylicRC()
        self.transmitter = Transmitter()
        pass


    def execute(self):
        pass
