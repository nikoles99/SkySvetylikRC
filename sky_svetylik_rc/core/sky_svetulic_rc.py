from constants.constants import MIDDLE_PULSE_WIDTH
from utils.config_utils import ConfigUtils


class SkySvetylicRC:

    def __init__(self, board):
        self.ESC_FORWARD_LEFT_GPIO = ConfigUtils.read_value('pinOut.esc.forwardLeft')
        self.ESC_BACKWARD_LEFT_GPIO = ConfigUtils.read_value('pinOut.esc.backwardLeft')
        self.ESC_BACKWARD_RIGHT_GPIO = ConfigUtils.read_value('pinOut.esc.backwardRight')
        self.ESC_FORWARD_RIGHT_GPIO = ConfigUtils.read_value('pinOut.esc.forwardRight')
        self.board = board
        pass

    def update(self, gas_pulse_width, yaw_pulse_width, pitch_pulse_width, roll_pulse_width):
        yaw_percents = self.compute_in_persents(yaw_pulse_width)
        pitch_percents = self.compute_in_persents(pitch_pulse_width)
        roll_percents = self.compute_in_persents(roll_pulse_width)
        gas_forward_left = gas_pulse_width + (gas_pulse_width * yaw_percents) + (gas_pulse_width * pitch_percents) + (gas_pulse_width * roll_percents)
        gas_forward_right = gas_pulse_width - (gas_pulse_width * yaw_percents) + (gas_pulse_width * pitch_percents) - (gas_pulse_width * roll_percents)
        gas_backward_left = gas_pulse_width - (gas_pulse_width * yaw_percents) - (gas_pulse_width * pitch_percents) + (gas_pulse_width * roll_percents)
        gas_backward_right = gas_pulse_width + (gas_pulse_width * yaw_percents) - (gas_pulse_width * pitch_percents) - (gas_pulse_width * roll_percents)
        self.gas(gas_forward_left, gas_forward_right, gas_backward_left, gas_backward_right)
        pass

    def gas(self, forward_left, forward_right, backward_left, backward_right):
        self.board.set_servo_pulsewidth(self.ESC_FORWARD_LEFT_GPIO, forward_left)
        self.board.set_servo_pulsewidth(self.ESC_FORWARD_RIGHT_GPIO, forward_right)
        self.board.set_servo_pulsewidth(self.ESC_BACKWARD_LEFT_GPIO, backward_left)
        self.board.set_servo_pulsewidth(self.ESC_BACKWARD_RIGHT_GPIO, backward_right)

    # Тангаж
    def pitch(self):
        pass

    # Крен
    def roll(self):
        pass

    # Рысканье
    def yaw(self):
        pass

    def compute_in_persents(self, yaw_pulse_width):
        if yaw_pulse_width == MIDDLE_PULSE_WIDTH:
            return yaw_pulse_width - MIDDLE_PULSE_WIDTH
        else:
            return (yaw_pulse_width - MIDDLE_PULSE_WIDTH) * 0.2 / 100
