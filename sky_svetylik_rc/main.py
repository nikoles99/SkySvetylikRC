import subprocess
import RPi.GPIO as GPIO
import logging
import os

from datetime import datetime
from core.fly_executor import FlyExecutor
from services.beeper import Beeper

# GPIO config
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Logger config
os.makedirs('logs', exist_ok=True)
file_handler = logging.FileHandler('logs/sky_svetylic_rc-{0}.log'
                                   .format(datetime.today().strftime('%Y-%m-%d-%H:%M:%S')))
formatter = logging.Formatter('[%(levelname)s]-%(asctime)s -- %(message)s')
file_handler.setFormatter(formatter)
logger = logging.getLogger('MAIN')
logger.addHandler(file_handler)

# Starting PWM pigpiod
process = subprocess.Popen('sudo pkill pigpiod;sudo pigpiod', stdout=subprocess.PIPE, shell=True)
output, error = process.communicate()
Beeper().init()


if error is None:
    FlyExecutor().execute()
else:
    logger.error(error)
    Beeper().error()
