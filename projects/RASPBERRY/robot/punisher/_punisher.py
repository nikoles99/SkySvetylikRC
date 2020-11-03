import RPi.GPIO as GPIO
import subprocess

PIN_17 = 17
PIN_27 = 27
DEFAULT_FREQUENCY = 50

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_17, GPIO.OUT)
GPIO.setup(PIN_27, GPIO.OUT)

left_wheel = GPIO.PWM(PIN_17, DEFAULT_FREQUENCY)   # GPIO 17 for PWM with 50Hz
left_wheel.start(2.5)                              # Initialization
right_wheel = GPIO.PWM(PIN_27, DEFAULT_FREQUENCY)  # GPIO 17 for PWM with 50Hz
right_wheel.start(2.5)


class _Punisher:

    def _move_forward(self):
        left_wheel.ChangeDutyCycle(70)
        right_wheel.ChangeDutyCycle(50)

    def _move_backward(self):
        left_wheel.ChangeDutyCycle(50)
        right_wheel.ChangeDutyCycle(70)

    def _turn_left(self):
        left_wheel.ChangeDutyCycle(50)
        right_wheel.ChangeDutyCycle(50)

    def _turn_right(self):
        left_wheel.ChangeDutyCycle(70)
        right_wheel.ChangeDutyCycle(70)

    def _stop(self):
        left_wheel.ChangeDutyCycle(0)
        right_wheel.ChangeDutyCycle(0)

    def _run(self):
        process = subprocess.Popen('irw', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        punisher = _Punisher()
        punisher._stop()

        try:
            while True:
                output = process.stdout.readline()
                print(output)
                if "KEY_RIGHT" in output:
                    punisher._turn_right()
                if "KEY_LEFT" in output:
                    punisher._turn_left()
                if "KEY_UP" in output:
                    punisher._move_forward()
                if "KEY_DOWN" in output:
                    punisher._move_backward()
                if "KEY_OK" in output:
                    punisher._stop()


        except KeyboardInterrupt:
            left_wheel._stop()
            right_wheel._stop()
            GPIO.cleanup()


punisher = _Punisher()
punisher._run()
