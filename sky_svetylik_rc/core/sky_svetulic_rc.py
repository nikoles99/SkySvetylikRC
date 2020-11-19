from constants.constants import GAS_MAX, GAS_MIN, YAW_MAX, YAW_MIN, PITCH_MAX, PITCH_MIN, ROLL_MAX, ROLL_MIN
from utils.config_utils import ConfigUtils

MIDDLE_PULSE_WIDTH = 1500


class SkySvetylicRC:

    def __init__(self, board):
        self.ESC_FORWARD_LEFT_GPIO = ConfigUtils.read_value('pinOut.esc.forwardLeft')
        self.ESC_BACKWARD_LEFT_GPIO = ConfigUtils.read_value('pinOut.esc.backwardLeft')
        self.ESC_BACKWARD_RIGHT_GPIO = ConfigUtils.read_value('pinOut.esc.backwardRight')
        self.ESC_FORWARD_RIGHT_GPIO = ConfigUtils.read_value('pinOut.esc.forwardRight')
        self.board = board
        pass

    def update(self, transmitter):
        yaw_percents = self.compute_in_percents(transmitter.yaw_pw, YAW_MIN, YAW_MAX)
        pitch_percents = self.compute_in_percents(transmitter.pitch_pw, PITCH_MIN, PITCH_MAX)
        roll_percents = self.compute_in_percents(transmitter.roll_pw, ROLL_MIN, ROLL_MAX)
        gas_percents = self.compute_in_percents(transmitter.gas_pw, GAS_MIN, GAS_MAX)

        gas_forward_left = transmitter.gas_pw + transmitter.gas_pw * (-yaw_percents - pitch_percents + roll_percents)
        gas_forward_right = transmitter.gas_pw + transmitter.gas_pw * (yaw_percents - pitch_percents - roll_percents)
        gas_backward_left = transmitter.gas_pw + transmitter.gas_pw * (yaw_percents + pitch_percents + roll_percents)
        gas_backward_right = transmitter.gas_pw + transmitter.gas_pw * (-yaw_percents + pitch_percents - roll_percents)
        print("{}                      {}                         {}                         {}"
              .format(gas_forward_left, gas_forward_right, gas_backward_left, gas_backward_right))
        self.gas(gas_forward_left, gas_forward_right, gas_backward_left, gas_backward_right)
        pass

    def gas(self, forward_left, forward_right, backward_left, backward_right):
        if forward_left > GAS_MAX:
            forward_left = GAS_MAX
        if forward_left < GAS_MIN:
            forward_left = GAS_MIN
        if forward_right > GAS_MAX:
            forward_right = GAS_MAX
        if forward_right < GAS_MIN:
            forward_right = GAS_MIN
        if backward_left > GAS_MAX:
            backward_left = GAS_MAX
        if backward_left < GAS_MIN:
            backward_left = GAS_MIN
        if backward_right > GAS_MAX:
            backward_right = GAS_MAX
        if backward_right < GAS_MIN:
            backward_right = GAS_MIN
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

    @staticmethod
    def compute_in_percents(current_pw, min_pw, max_pw):
        average_pw = (max_pw + min_pw) / 2
        if current_pw == average_pw:
            return 0
        else:
            return (current_pw - average_pw) * 0.002
