import logging
import time
import pigpio

from constants.constants import APP_NAME
from exceptions.no_receiver_connection_exception import NoReceiverConnectionException
from services.receiver_pwm_reader import ReceiverPMWReader
from services.beeper import Beeper
from core.sky_svetulic_rc import SkySvetylicRC
from utils.config_utils import ConfigUtils


class Executor:

    # process = subprocess.Popen('sudo shutdown now', stdout=subprocess.PIPE, shell=True)
    # output, error = process.communicate()

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
                frequency = self.receiver_left_vertical.frequency()
                pulse_width = self.receiver_left_vertical.pulse_width()
                duty_cycle = self.receiver_left_vertical.duty_cycle()
                self.drone.gas(pulse_width)
                print("frequency={:.1f} pulse_width={} duty_cycle={:.2f}"
                      .format(frequency, int(pulse_width + 0.5), duty_cycle))
        except Exception as exception:
            Beeper().error()
            self.logger.error(exception)
            self.receiver_left_vertical.cancel()
            self.receiver_left_horizontal.cancel()
            self.receiver_right_vertical.cancel()
            self.receiver_right_horizontal.cancel()
            # Beeper.turn_off()
        finally:
            self.drone.gas(1000)

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
