import subprocess
import RPi.GPIO as GPIO
import logging

from core.fly_executor import FlyExecutor
from services.beeper import Beeper

# GPIO config
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Logger config
logger = logging.getLogger('MAIN')
logging.basicConfig(filename='sky_svetylic_rc.log', filemode='w', format='[%(levelname)s]-%(asctime)s -- %(message)s',
                    level=logging.DEBUG, datefmt='%d-%b-%y %H:%M:%S')

# Starting PWM pigpiod
process = subprocess.Popen('sudo pkill pigpiod;sudo pigpiod',
                           stdout=subprocess.PIPE, shell=True)
output, error = process.communicate()
Beeper().init()


if error is None:
    FlyExecutor().execute()
else:
    logger.error(error)
    Beeper().error()
