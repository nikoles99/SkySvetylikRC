class PIDRegulator:

    def __init__(self, P_gain, I_gain, D_gain):
        self.P_gain = P_gain
        self.I_gain = I_gain
        self.D_gain = D_gain
        self.P_output = 0
        self.I_output = 0
        self.D_output = 0
        self.error = 0
        self.OUTPUT_THRESHOLD = 200
        pass

    def regulate(self, gyro, receiver):
        error_previous = self.error
        self.error = gyro - receiver
        self.P_output = self.P_gain * self.error
        self.I_output += self.I_gain * self.error
        self.D_output = (self.error - error_previous)
        output = self.P_output + self.I_output + self.D_gain * self.D_output
        return self.restrict_output(output)

    def restrict_output(self, output):
        if output > self.OUTPUT_THRESHOLD:
            return self.OUTPUT_THRESHOLD
        if output < -self.OUTPUT_THRESHOLD:
            return -self.OUTPUT_THRESHOLD
        return output

    def reset(self):
        self.I_output = 0
        self.error = 0
