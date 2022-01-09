from constants.constants import GAS_MIN, YAW_MAX, OFFSET_PW, UN_PLUGIN_PW
from core.executor import Executor
from exceptions.no_receiver_connection_exception import NoReceiverConnectionException
from services.beeper import Beeper
from utils.camera import Camera


class FlyExecutor(Executor):

    def __init__(self):
        super().__init__()
        self.camera = Camera()
        self.isArmed = True

    def execute(self):
        self.drone.gas_off()
        self.arm()
        while True:
            try:
                if not self.is_transmitter_available():
                    raise NoReceiverConnectionException('Receiver connection has lost')
                if self.is_stick_bottom_left():
                    self.drone.gas_off()
                    self.arm()
                self.drone.update(self.transmitter)
            except Exception as exception:
                self.drone.gas_off()
                Beeper().error()
                self.logger.error(exception)
                self.arm()

    def arm(self):
        Beeper().init()
        self.logger.info('START')
        while True:
            if not self.is_transmitter_available():
                Beeper().search()
                continue
            if self.is_stick_bottom_left():
                Beeper().start()
                self.isArmed = not self.isArmed
                self.switch_camera_mode()
                break

    def is_stick_bottom_left(self):
        return self.transmitter.gas_pw - GAS_MIN <= OFFSET_PW and YAW_MAX - self.transmitter.yaw_pw <= OFFSET_PW

    def is_transmitter_available(self):
        return self.is_signal_available(self.transmitter.gas_pw) and self.is_signal_available(self.transmitter.yaw_pw) \
               and self.is_signal_available(self.transmitter.pitch_pw) and self.is_signal_available(self.transmitter.roll_pw)

    def is_signal_available(self, signal):
        return signal != 0 and signal > UN_PLUGIN_PW

    def switch_camera_mode(self):
        try:
            if self.isArmed:
                self.camera.stop_recording()
            else:
                self.camera.start_recording()
        except Exception as exception:
            self.logger.error(exception)

    def turn_off(self):
        Beeper().turn_off()