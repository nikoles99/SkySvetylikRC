from machine import Pin , PWM
from utils.config_utils import ConfigUtils


class Transmitter:

    def __init__(self, board):
        self.gas_pw = PWM(Pin(ConfigUtils.read_value('pinIn.reciever.leftVercical')))
        self.gas_pw(100000)  
        self.gas_pw(32768)
        
        self.yaw_pw = PWM(Pin(ConfigUtils.read_value('pinIn.reciever.leftHorizontal')))
        self.yaw_pw(100000)  
        self.yaw_pw(32768)
        
        self.pitch_pw = PWM(Pin(ConfigUtils.read_value('pinIn.reciever.rightVertical')))
        self.pitch_pw(100000)  
        self.pitch_pw(32768)
        
        self.roll_pw = PWM(Pin(ConfigUtils.read_value('pinIn.reciever.rightHorizontal')))
        self.roll_pw(100000)  
        self.roll_pw(32768)
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
