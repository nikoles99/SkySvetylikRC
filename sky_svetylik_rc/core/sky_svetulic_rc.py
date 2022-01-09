import time

from constants.constants import GAS_MAX, GAS_MIN, GAS_FLY_MIN, YAW_MAX, YAW_MIN, PITCH_MAX, PITCH_MIN, ROLL_MAX, ROLL_MIN, OFFSET_PW
from pid.pid_regulator import PIDRegulator
from services.tilts_meter import TiltsMeter
from utils.config_utils import ConfigUtils


class SkySvetylicRC:

    def __init__(self):
        self.ESC_FORWARD_LEFT_GPIO = ConfigUtils.read_value('pinOut.esc.forwardLeft')
        self.ESC_BACKWARD_LEFT_GPIO = ConfigUtils.read_value('pinOut.esc.backwardLeft')
        self.ESC_BACKWARD_RIGHT_GPIO = ConfigUtils.read_value('pinOut.esc.backwardRight')
        self.ESC_FORWARD_RIGHT_GPIO = ConfigUtils.read_value('pinOut.esc.forwardRight')

        self.roll_P = ConfigUtils.read_value('roll.P')
        self.roll_I = ConfigUtils.read_value('roll.I')
        self.roll_D = ConfigUtils.read_value('roll.D')
        self.roll_regulator = PIDRegulator(self.roll_P, self.roll_I, self.roll_D)

        self.pitch_P = ConfigUtils.read_value('pitch.P')
        self.pitch_I = ConfigUtils.read_value('pitch.I')
        self.pitch_D = ConfigUtils.read_value('pitch.D')
        self.pitch_regulator = PIDRegulator(self.pitch_P, self.pitch_I, self.pitch_D)

        self.yaw_P = ConfigUtils.read_value('yaw.P')
        self.yaw_I = ConfigUtils.read_value('yaw.I')
        self.yaw_D = ConfigUtils.read_value('yaw.D')
        self.yaw_regulator = PIDRegulator(self.yaw_P, self.yaw_I, self.yaw_D)

        self.board = null
        self.tilts_meter = TiltsMeter()
        self.cycle_time = 0
        self.start_gas = GAS_MIN + 100
        self.yaw_middle_pw = (YAW_MAX + YAW_MIN) / 2
        pass

    def update(self, transmitter):
        time_time = time.perf_counter()
        angles = self.tilts_meter.get_yaw_pitch_roll_angles(self.cycle_time)
        regulated_roll = self.roll_regulator.regulate(angles.roll, self.pulse_to_degree(transmitter.roll_pw, ROLL_MIN, ROLL_MAX))
        regulated_pitch = self.pitch_regulator.regulate(angles.pitch, self.pulse_to_degree(transmitter.pitch_pw, PITCH_MIN, PITCH_MAX))
        yaw_degree = self.pulse_to_degree(transmitter.yaw_pw, YAW_MIN, YAW_MAX)
        regulated_yaw = self.regulate_yaw(angles.yaw, yaw_degree, transmitter)
        gas_forward_left = transmitter.gas_pw - regulated_roll + regulated_pitch + regulated_yaw
        gas_forward_right = transmitter.gas_pw + regulated_roll + regulated_pitch - regulated_yaw
        gas_backward_left = transmitter.gas_pw - regulated_roll - regulated_pitch - regulated_yaw
        gas_backward_right = transmitter.gas_pw + regulated_roll - regulated_pitch + regulated_yaw
        self.gas(gas_forward_left, gas_forward_right, gas_backward_left, gas_backward_right)
        self.cycle_time = time.perf_counter() - time_time
        pass

    def regulate_yaw(self, yaw, yaw_degree, transmitter):
        if (abs(self.yaw_middle_pw - transmitter.yaw_pw) >= 20 * OFFSET_PW) or (transmitter.gas_pw - GAS_MIN <= OFFSET_PW):
            self.yaw_regulator.reset()
            self.tilts_meter.reset_yaw_angle()
            return -4 * yaw_degree
        return self.yaw_regulator.regulate(yaw, yaw_degree)

    def gas(self, forward_left, forward_right, backward_left, backward_right):
        forward_left = self.restrict_input_pw(forward_left)
        forward_right = self.restrict_input_pw(forward_right)
        backward_left = self.restrict_input_pw(backward_left)
        backward_right = self.restrict_input_pw(backward_right)
        self.board.set_servo_pulsewidth(self.ESC_FORWARD_LEFT_GPIO, forward_left)
        self.board.set_servo_pulsewidth(self.ESC_FORWARD_RIGHT_GPIO, forward_right)
        self.board.set_servo_pulsewidth(self.ESC_BACKWARD_LEFT_GPIO, backward_left)
        self.board.set_servo_pulsewidth(self.ESC_BACKWARD_RIGHT_GPIO, backward_right)

    def restrict_input_pw(self, input_pw):
        if input_pw > GAS_MAX:
            input_pw = GAS_MAX
        if input_pw < GAS_FLY_MIN:
            input_pw = GAS_FLY_MIN
        return input_pw

    def gas_off(self):
        self.board.set_servo_pulsewidth(self.ESC_FORWARD_LEFT_GPIO, GAS_MIN)
        self.board.set_servo_pulsewidth(self.ESC_FORWARD_RIGHT_GPIO, GAS_MIN)
        self.board.set_servo_pulsewidth(self.ESC_BACKWARD_LEFT_GPIO, GAS_MIN)
        self.board.set_servo_pulsewidth(self.ESC_BACKWARD_RIGHT_GPIO, GAS_MIN)
        self.roll_regulator.reset()
        self.pitch_regulator.reset()
        self.yaw_regulator.reset()
        self.tilts_meter.reset_yaw_angle()

    def get_gas(self, gas):
        if gas < self.start_gas:
            return self.start_gas
        return gas

    @staticmethod
    def pulse_to_degree(pulse_value, min_pw, max_pw):
        average_pw = (max_pw + min_pw) / 2
        pw_ = (pulse_value - average_pw) / 16.6
        return int(round(pw_))

    @staticmethod
    def degree_to_pulse(degree_value):
        return degree_value * 15

    @staticmethod
    def compute_in_percents(current_pw, min_pw, max_pw):
        average_pw = (max_pw + min_pw) / 2
        if current_pw == average_pw:
            return 0
        else:
            return (current_pw - average_pw) * 0.002