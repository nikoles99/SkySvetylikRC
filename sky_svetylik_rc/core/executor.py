import logging
import time
import subprocess

import pigpio

from constants.constants import APP_NAME
from exceptions.no_receiver_connection_exception import NoReceiverConnectionException
from services.receiver_pwm_reader import ReceiverPMWReader
from services.beeper import Beeper
from core.sky_svetulic_rc import SkySvetylicRC
from utils.config_utils import ConfigUtils


class Executor:

    def __init__(self):
        self.start = time.time()
        self.RUN_TIME = 60.0
        self.SAMPLE_TIME = 1.0
        self.board = pigpio.pi()
        self.drone = SkySvetylicRC(self.board)
        self.receiver_left_vertical = ReceiverPMWReader(self.board,
                                                        ConfigUtils.readValue('pinIn.reciever.leftVercical'))
        self.receiver_left_horizontal = ReceiverPMWReader(self.board,
                                                          ConfigUtils.readValue('pinIn.reciever.leftHorizontal'))
        self.receiver_right_vertical = ReceiverPMWReader(self.board,
                                                         ConfigUtils.readValue('pinIn.reciever.rightVertical'))
        self.receiver_right_horizontal = ReceiverPMWReader(self.board,
                                                           ConfigUtils.readValue('pinIn.reciever.rightHorizontal'))
        self.logger = logging.getLogger(APP_NAME)
        pass

    def execute(self):
        try:
            self.safe_init()
            while (time.time() - self.start) < self.RUN_TIME:
                #frequency = self.receiver_left_vertical.frequency()
                #duty_cycle = self.receiver_left_vertical.duty_cycle()
                receiver_left_vertical_pulse_width = self.receiver_left_vertical.pulse_width()
                receiver_left_horizontal_pulse_width = self.receiver_left_horizontal.pulse_width()
                receiver_right_vertical_pulse_width = self.receiver_right_vertical.pulse_width()
                receiver_right_horizontal_pulse_width = self.receiver_right_horizontal.pulse_width()
                self.drone.update(receiver_left_vertical_pulse_width, receiver_left_horizontal_pulse_width, receiver_right_vertical_pulse_width, receiver_right_horizontal_pulse_width)
                print("lv={} lh={} rh={} rl{}".format(receiver_left_vertical_pulse_width, receiver_left_horizontal_pulse_width, receiver_right_vertical_pulse_width, receiver_right_horizontal_pulse_width))
                #print("frequency={:.1f} receiver_left_vertical_pulse_width={} duty_cycle={:.2f}"
                #      .format('frequency', int(receiver_left_vertical_pulse_width + 0.5), 'duty_cycle'))
        except Exception as exception:
            self.drone.gas(1000, 1000, 1000, 1000)
            self.logger.error(exception)
            self.receiver_left_vertical.cancel()
            self.receiver_left_horizontal.cancel()
            self.receiver_right_vertical.cancel()
            self.receiver_right_horizontal.cancel()
        finally:
            Beeper().error()
            self.drone.gas(1000, 1000, 1000, 1000)

    def safe_init(self):
        # check sticks in bottom left positions
        Beeper().init()
        self.logger.info('START')
        while True:
            pulse_width1 = self.receiver_left_vertical.pulse_width()
            pulse_width2 = self.receiver_left_horizontal.pulse_width()
            pulse_width3 = self.receiver_right_vertical.pulse_width()
            pulse_width4 = self.receiver_right_horizontal.pulse_width()
            if pulse_width1 == 0 or pulse_width2 == 0 or pulse_width3 == 0 or pulse_width4 == 0:
                raise NoReceiverConnectionException()
            if pulse_width1 < 1010 and pulse_width2 < 1010 and pulse_width3 < 1010 and pulse_width4 < 1010:
                Beeper().start()
                break

    @staticmethod
    def turn_off():
        Beeper().turn_off()
        subprocess.Popen('sudo shutdown now', stdout=subprocess.PIPE, shell=True).communicate()
