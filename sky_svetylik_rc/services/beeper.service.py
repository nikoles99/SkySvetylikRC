import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
buzzer = 23
GPIO.setup(buzzer, GPIO.OUT)

class Beeper:

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        buzzer = 23
        GPIO.setup(buzzer, GPIO.OUT)
        pass

while True:
    GPIO.output(buzzer, GPIO.HIGH)
    print ("Beep")
    sleep(0.5)  # Delay in seconds
    GPIO.output(buzzer, GPIO.LOW)
    print ("No Beep")
    sleep(0.5)


