class GyroAccelModel:

    def __init__(self, roll=0, pitch=0, yaw=0):
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
        pass

    @property
    def roll(self):
        return self.__roll

    @property
    def pitch(self):
        return self.__pitch

    @property
    def yaw(self):
        return self.__yaw

    @roll.setter
    def roll(self, value):
        self.__roll = value

    @pitch.setter
    def pitch(self, value):
        self.__pitch = value

    @yaw.setter
    def yaw(self, value):
        self.__yaw = value
