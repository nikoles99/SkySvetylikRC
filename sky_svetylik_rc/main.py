import subprocess
import RPi.GPIO as GPIO
import logging

from constants.constants import APP_NAME
from core.executor import Executor
from services.beeper import Beeper

# GPIO config
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Logger config
logger = logging.getLogger(APP_NAME)
logging.basicConfig(filename='sky_svetylic_rc.log', filemode='w', format='[%(levelname)s]-%(asctime)s -- %(message)s',
                    level=logging.DEBUG, datefmt='%d-%b-%y %H:%M:%S')

# Starting PWM pigpiod
process = subprocess.Popen('sudo killall pigpiod;sudo pigpiod', stdout=subprocess.PIPE, shell=True)
output, error = process.communicate()

if error is None:
    Executor().execute()
else:
    logger.error(error)
    Beeper().error()
