import RPi.GPIO as GPIO
import time
import subprocess

servoPIN17 = 17
servoPIN27 = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN17, GPIO.OUT)
GPIO.setup(servoPIN27, GPIO.OUT)

p17 = GPIO.PWM(servoPIN17, 50)  # GPIO 17 for PWM with 50Hz
p17.start(2.5)  # Initialization
p27 = GPIO.PWM(servoPIN27, 50)  # GPIO 17 for PWM with 50Hz
p27.start(2.5)


class Punisher:

    def move_forward(self):
        p17.ChangeDutyCycle(70)
        p27.ChangeDutyCycle(50)

    def move_backward(self):
        p17.ChangeDutyCycle(50)
        p27.ChangeDutyCycle(70)

    def turn_left(self):
        p17.ChangeDutyCycle(50)
        p27.ChangeDutyCycle(50)

    def turn_right(self):
        p17.ChangeDutyCycle(70)
        p27.ChangeDutyCycle(70)

    def stop(self):
        p17.ChangeDutyCycle(0)
        p27.ChangeDutyCycle(0)


def run_punisher():
    p = subprocess.Popen('irw', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    punisher = Punisher()
    punisher.stop()
    
    try:
        while True:
            line = p.stdout.readline()
            print(line)
            if "KEY_RIGHT" in line:
                punisher.turn_right()
            if "KEY_LEFT" in line:
                punisher.turn_left()
            if "KEY_UP" in line:
                punisher.move_forward()
            if "KEY_DOWN" in line:
                punisher.move_backward()
            if "KEY_OK" in line:
                punisher.stop()


    except KeyboardInterrupt:
        p17.stop()
        p27.stop()
        GPIO.cleanup()


run_punisher()
