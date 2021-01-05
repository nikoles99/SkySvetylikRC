class PIDRegulator:

    def __init__(self, P_gain, I_gain, D_gain):
        self.P_gain = P_gain
        self.I_gain = I_gain
        self.D_gain = D_gain
        self.P_output = 0
        self.I_output = 0
        self.D_output = 0
        self.error = 0
        pass

    def regulate(self, gyro, receiver, transmitter):
        # self.I_gain = (transmitter.switcher_right_pw-1000)/1000
        # self.D_gain = (transmitter.switcher_left_pw-1000)/50
        # print(self.I_gain, self.D_gain, gyro)
        error_previous = self.error
        self.error = gyro - receiver
        self.P_output = self.P_gain * self.error
        self.I_output += self.I_gain * self.error
        if self.I_output > 400:
            self.I_output = 400
        if self.I_output < -400:
            self.I_output = -400
        self.D_output = (self.error - error_previous)
        # print(receiver,      gyro)
        output = self.P_output + self.I_output + self.D_gain * self.D_output
        if output > 400:
            output = 400
        if output < -400:
            output = -400
        # print(receiver,          gyro)
        return output

    def reset(self):
        self.I_output = 0
        self.error = 0
