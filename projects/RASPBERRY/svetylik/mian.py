import time

import RPi.GPIO as GPIO
import pigpio
from time import sleep

from sygnal_test import PWMReader

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT)
pwm = GPIO.PWM(4, 50)
pwm.start(0)

GPIO.setup(14, GPIO.OUT)
pwm1 = GPIO.PWM(14, 100)
pwm1.start(0)

GPIO.setup(15, GPIO.OUT)
pwm2 = GPIO.PWM(15, 100)
pwm2.start(0)

GPIO.setup(18, GPIO.OUT)
pwm3 = GPIO.PWM(18, 100)
pwm3.start(0)

PWM_GPIO = 3
RUN_TIME = 60.0
SAMPLE_TIME = 1.0

pi = pigpio.pi()
p = PWMReader(pi, PWM_GPIO)
start = time.time()

while (time.time() - start) < RUN_TIME:
    #time.sleep(SAMPLE_TIME)
    f = p.frequency()
    pw = p.pulse_width()
    dc = p.duty_cycle()
    if pw > 1000:
        pw_ = (pw - 1000) / 10
        if pw_ < 1:
            pw_ = 0
        if pw_ > 100:
            pw_ = 100
        pwm.ChangeDutyCycle(pw_)
        pwm1.ChangeDutyCycle(pw_)
        pwm2.ChangeDutyCycle(pw_)
        pwm3.ChangeDutyCycle(pw_)
       # pi.set_servo_pulsewidth(4, pw)
        #pi.set_servo_pulsewidth(14, pw)
        #pi.set_servo_pulsewidth(15, 1500)
        #pi.set_servo_pulsewidth(18, pw)

    print("f={:.1f} pw={} dc={:.2f}".format(f, int(pw + 0.5), dc))

p.cancel()
pi.stop()
