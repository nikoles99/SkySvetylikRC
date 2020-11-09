from utils.config_utils import ConfigUtils


class SkySvetylicRC:

    def __init__(self, board):
        self.ESC_FORWARD_LEFT_GPIO = ConfigUtils.readValue('pinOut.esc.forwardLeft')
        self.ESC_BACKWARD_LEFT_GPIO = ConfigUtils.readValue('pinOut.esc.backwardLeft')
        self.ESC_BACKWARD_RIGHT_GPIO = ConfigUtils.readValue('pinOut.esc.backwardRight')
        self.ESC_FORWARD_RIGHT_GPIO = ConfigUtils.readValue('pinOut.esc.forwardRight')
        self.board = board
        pass

    def gas(self, pulse_width):
        self.board.set_servo_pulsewidth(self.ESC_FORWARD_LEFT_GPIO, pulse_width)
        self.board.set_servo_pulsewidth(self.ESC_BACKWARD_LEFT_GPIO, pulse_width)
        self.board.set_servo_pulsewidth(self.ESC_BACKWARD_RIGHT_GPIO, pulse_width)
        self.board.set_servo_pulsewidth(self.ESC_FORWARD_RIGHT_GPIO, pulse_width)

    # Тангаж
    def pitch(self):
        pass

    # Крен
    def roll(self):
        pass

    # Рысканье
    def yaw(self):
        pass
