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

    def regulate(self, gyro, receiver, time):
        error_previous = self.error
        self.error = receiver - gyro
        self.P_output = self.P_gain * self.error
        self.I_output += self.I_gain * self.error * time
        self.D_output = self.D_gain * (self.error - error_previous) / time
        print(self.P_output,      self.I_output,       self.D_output)
        return self.P_output + self.I_output + self.D_output
