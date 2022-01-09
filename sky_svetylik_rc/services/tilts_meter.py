from libs.imu import MPU6050
import time
from machine import Pin, I2C


from domain.gyro_accel_model import GyroAccelModel


# sudo i2cdetect -y 1


class TiltsMeter:
    gyro_x_error = 0
    gyro_y_error = 0
    gyro_z_error = 0
    accel_x_error = 0
    accel_y_error = 0

    angle_roll = 0
    angle_pitch = 0
    angle_yaw = 0
    first_reading = True
    previous_time = 0

    def __init__(self, address=0x68):
        i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
        imu = MPU6050(i2c)
        self.calibrate()


    def calibrate(self):
        accel_x_sum = 0
        accel_y_sum = 0
        gyro_x_sum = 0
        gyro_y_sum = 0
        gyro_z_sum = 0
        CALIBRATION_RANGE = 2000

        for i in range(CALIBRATION_RANGE):
            accel_x_out, accel_y_out, accel_z_out = self.get_accel_data()
            accel_x = self.get_x_rotation(accel_x_out, accel_y_out, accel_z_out)
            accel_y = self.get_y_rotation(accel_x_out, accel_y_out, accel_z_out)
            accel_x_sum = accel_x_sum + accel_x
            accel_y_sum = accel_y_sum + accel_y
            gyro_x_out, gyro_y_out, gyro_z_out = self.get_gyro_data()
            gyro_x_sum = gyro_x_sum + gyro_x_out
            gyro_y_sum = gyro_y_sum + gyro_y_out
            gyro_z_sum = gyro_z_sum + gyro_z_out

        self.accel_x_error = accel_x_sum / CALIBRATION_RANGE
        self.accel_y_error = accel_y_sum / CALIBRATION_RANGE
        self.gyro_x_error = gyro_x_sum / CALIBRATION_RANGE
        self.gyro_y_error = gyro_y_sum / CALIBRATION_RANGE
        self.gyro_z_error = gyro_z_sum / CALIBRATION_RANGE

    def get_y_rotation(self, x, y, z):
        radians = math.atan2(x, self.dist(y, z))
        return -math.degrees(radians)

    def get_x_rotation(self, x, y, z):
        radians = math.atan2(y, self.dist(x, z))
        return math.degrees(radians)

    def dist(self, a, b):
        return math.sqrt((a * a) + (b * b))

    def reset_yaw_angle(self):
        self.angle_yaw = 0

    def get_yaw_pitch_roll_angles(self, cycle_time):
        gyro_x_out, gyro_y_out, gyro_z_out = self.get_gyro_data()
        self.angle_roll = self.angle_roll + (gyro_x_out - self.gyro_x_error) * cycle_time
        self.angle_pitch = self.angle_pitch + (gyro_y_out - self.gyro_y_error) * cycle_time
        angle_yaw_split_second = (gyro_z_out - self.gyro_z_error) * cycle_time
        self.angle_yaw = self.angle_yaw - angle_yaw_split_second

        angle_yaw_sin = math.sin(angle_yaw_split_second * 3.142 / 180)
        self.angle_roll += self.angle_pitch * angle_yaw_sin
        self.angle_pitch -= self.angle_roll * angle_yaw_sin

        accel_x_out, accel_y_out, accel_z_out = self.get_accel_data()
        accel_x = self.get_x_rotation(accel_x_out, accel_y_out, accel_z_out) - self.accel_x_error
        accel_y = self.get_y_rotation(accel_x_out, accel_y_out, accel_z_out) - self.accel_y_error

        if not self.first_reading:
            self.angle_roll = self.angle_roll * 0.99 + accel_x * 0.01
            self.angle_pitch = self.angle_pitch * 0.99 + accel_y * 0.01
        else:
            self.angle_roll = accel_x
            self.angle_pitch = accel_y
            self.first_reading = False
        return GyroAccelModel(self.angle_roll, self.angle_pitch, self.angle_yaw)
