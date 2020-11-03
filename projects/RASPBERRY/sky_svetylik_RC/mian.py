import time

import pigpio

from pwm_reader import PWMReader

PWM_GPIO = 3
RUN_TIME = 60.0
SAMPLE_TIME = 1.0

pi = pigpio.pi()
p = PWMReader(pi, PWM_GPIO)
start = time.time()

while (time.time() - start) < RUN_TIME:
    f = p.frequency()
    pw = p.pulse_width()
    dc = p.duty_cycle()
    pi.set_servo_pulsewidth(4, pw)
    pi.set_servo_pulsewidth(14, pw)
    pi.set_servo_pulsewidth(15, pw)
    pi.set_servo_pulsewidth(18, pw)
    print("f={:.1f} pw={} dc={:.2f}".format(f, int(pw + 0.5), dc))

p.cancel()
pi._stop()
