import time

from constants.constants import GAS_MAX, GAS_MIN, YAW_MAX, YAW_MIN, PITCH_MAX, PITCH_MIN, ROLL_MAX, ROLL_MIN, ERROR_MS
from pid.pid_regulator import PIDRegulator
from services.tilts_meter import TiltsMeter
from utils.config_utils import ConfigUtils


class SkySvetylicRC:

    def __init__(self, board):
        self.ESC_FORWARD_LEFT_GPIO = ConfigUtils.read_value('pinOut.esc.forwardLeft')
        self.ESC_BACKWARD_LEFT_GPIO = ConfigUtils.read_value('pinOut.esc.backwardLeft')
        self.ESC_BACKWARD_RIGHT_GPIO = ConfigUtils.read_value('pinOut.esc.backwardRight')
        self.ESC_FORWARD_RIGHT_GPIO = ConfigUtils.read_value('pinOut.esc.forwardRight')
        self.board = board
        self.tilts_meter = TiltsMeter()
        self.cycle_time = 0.02

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
        self.move_min_gas = GAS_MIN + ERROR_MS + 5
        pass

    def update(self, transmitter):
        time_time = time.process_time()
        angles = self.tilts_meter.get_yaw_pitch_roll_angles()
        regulated_roll = self.roll_regulator.regulate(angles.roll, self.pulse_to_degree(transmitter.roll_pw, ROLL_MIN, ROLL_MAX), self.cycle_time)
        regulated_pitch = self.pitch_regulator.regulate(angles.pitch, self.pulse_to_degree(transmitter.pitch_pw, PITCH_MIN, PITCH_MAX), self.cycle_time)
        regulated_yaw = self.yaw_regulator.regulate(angles.yaw, self.pulse_to_degree(transmitter.yaw_pw, YAW_MIN, YAW_MAX), self.cycle_time)
        regulated_roll = self.degree_to_pulse(regulated_roll)
        regulated_pitch = self.degree_to_pulse(regulated_pitch)
        regulated_yaw = self.degree_to_pulse(regulated_yaw)

        gas_forward_left = transmitter.gas_pw + regulated_roll - regulated_pitch  # - regulated_yaw
        gas_forward_right = transmitter.gas_pw - regulated_roll - regulated_pitch  # + regulated_yaw
        gas_backward_left = transmitter.gas_pw + regulated_roll + regulated_pitch  # + regulated_yaw
        gas_backward_right = transmitter.gas_pw - regulated_roll + regulated_pitch  # - regulated_yaw
        if transmitter.gas_pw > self.move_min_gas:
            self.gas(gas_forward_left, gas_forward_right, gas_backward_left, gas_backward_right)
        else:
            self.gas(GAS_MIN, GAS_MIN, GAS_MIN, GAS_MIN)
        self.cycle_time = time.process_time() - time_time
        # print("{}, {}, {}, {}, {}", self.cycle_time, angles.roll, angles.pitch, regulated_roll, angles.yaw  )
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

    @staticmethod
    def pulse_to_degree(pulse_value, min_pw, max_pw):
        average_pw = (max_pw + min_pw) / 2
        return (pulse_value - average_pw) / 3

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
