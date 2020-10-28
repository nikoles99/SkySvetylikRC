import time

import RPi.GPIO as GPIO
import pigpio

from sygnal_test import PWMReader

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(24, GPIO.OUT)
pwm = GPIO.PWM(24, 100)

PWM_GPIO = 4
RUN_TIME = 60.0
SAMPLE_TIME = 2.0

pi = pigpio.pi()
p = PWMReader(pi, PWM_GPIO)
start = time.time()

while (time.time() - start) < RUN_TIME:
    # time.sleep(SAMPLE_TIME)

    f = p.frequency()
    pw = p.pulse_width()
    dc = p.duty_cycle()
    if pw > 1000:
        pw_ = (pw - 1000) / 10
        if pw_ < 0:
            pw_ = 0
        if pw_ > 100:
            pw_ = 100
        pwm.ChangeDutyCycle(pw_)
    print("f={:.1f} pw={} dc={:.2f}".format(f, int(pw + 0.5), dc))

p.cancel()
pi.stop()
