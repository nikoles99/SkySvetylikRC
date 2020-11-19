class StickRange:
    def __init__(self, min_value=1500, max_value=1500):
        self.min = min_value
        self.max = max_value
        pass

    @property
    def min(self):
        return self.__min

    @property
    def max(self):
        return self.__max

    @min.setter
    def min(self, value):
        self.__min = value

    @max.setter
    def max(self, value):
        self.__max = value
