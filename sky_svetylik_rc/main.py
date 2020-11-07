import subprocess
import RPi.GPIO as GPIO
import logging

from constants.constants import APP_NAME
from core.executor import Executor
from services.beeper import Beeper

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.ERROR)

# Starting PWM pigpiod
process = subprocess.Popen('sudo killall pigpiod;sudo pigpiod', stdout=subprocess.PIPE, shell=True)
output, error = process.communicate()

if error is None:
    Executor().execute()
else:
    logger.error(error)
    Beeper().error()
