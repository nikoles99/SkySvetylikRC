from services.receiver_pwm_reader import ReceiverPMWReader
from utils.config_utils import ConfigUtils


class Transmitter:

    def __init__(self, board):
        self.gas_pw = ReceiverPMWReader(board, ConfigUtils.read_value('pinIn.reciever.leftVercical'))
        self.yaw_pw = ReceiverPMWReader(board, ConfigUtils.read_value('pinIn.reciever.leftHorizontal'))
        self.pitch_pw = ReceiverPMWReader(board, ConfigUtils.read_value('pinIn.reciever.rightVertical'))
        self.roll_pw = ReceiverPMWReader(board, ConfigUtils.read_value('pinIn.reciever.rightHorizontal'))
        # self.switcher_left_pw = ReceiverPMWReader(board, ConfigUtils.read_value('pinIn.reciever.switcherLeft'))
        # self.switcher_right_pw = ReceiverPMWReader(board, ConfigUtils.read_value('pinIn.reciever.switcherRight'))
        # frequency = self.receiver_left_vertical.frequency()
        # duty_cycle = self.receiver_left_vertical.duty_cycle()
        pass

    @property
    def gas_pw(self):
        return self.__gas_pw.pulse_width()

    @property
    def yaw_pw(self):
        return self.__yaw_pw.pulse_width()

    @property
    def pitch_pw(self):
        return self.__pitch_pw.pulse_width()

    @property
    def roll_pw(self):
        return self.__roll_pw.pulse_width()

    @property
    def switcher_left_pw(self):
        return self.__switcher_left_pw.pulse_width()

    @property
    def switcher_right_pw(self):
        return self.__switcher_right_pw.pulse_width()

    @yaw_pw.setter
    def yaw_pw(self, value):
        self.__yaw_pw = value

    @gas_pw.setter
    def gas_pw(self, value):
        self.__gas_pw = value

    @pitch_pw.setter
    def pitch_pw(self, value):
        self.__pitch_pw = value

    @roll_pw.setter
    def roll_pw(self, value):
        self.__roll_pw = value

    @switcher_left_pw.setter
    def switcher_left_pw(self, value):
        self.__switcher_left_pw = value

    @switcher_right_pw.setter
    def switcher_right_pw(self, value):
        self.__switcher_right_pw = value
