from utils.config_utils import ConfigUtils


class PIDRegulator:

    def __init__(self):
        self.P_gain = ConfigUtils.read_value('roll.P')
        self.I_gain = ConfigUtils.read_value('roll.I')
        self.D_gain = ConfigUtils.read_value('roll.D')
        self.P_output = 0
        self.I_output = 0
        self.D_output = 0
        self.error = 0
        pass

    def regulate(self, gyro, receiver, time):
        error_previous = self.error
        self.error = gyro - receiver
        self.P_output = self.P_gain * self.error
        self.I_output = (self.I_output + self.I_gain * self.error) * time
        self.D_output = self.D_output * (self.error - error_previous) / time
        return self.P_output + self.I_output + self.D_output
