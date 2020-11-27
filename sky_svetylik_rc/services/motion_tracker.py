import math
import time

import smbus

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

bus = smbus.SMBus(1)  # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68


def read_byte(adr):
    return bus.read_byte_data(address, adr)


def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr + 1)
    val = (high << 8) + low
    return val


def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val


def dist(a, b):
    return math.sqrt((a * a) + (b * b))


def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


previous_time = time.time()
gyroX = 0
gyroY = 0
yaw = 0

while True:
    try:
        current_time = time.time()
        elapsed_time = current_time - previous_time
        previous_time = current_time

        gyroskop_xout = read_word_2c(0x43) / 131
        gyroskop_yout = read_word_2c(0x45) / 131
        gyroskop_zout = read_word_2c(0x47) / 131

        gyroX = gyroskop_xout + gyroskop_xout * elapsed_time
        gyroY = gyroskop_yout + gyroskop_yout * elapsed_time
        yaw = gyroskop_zout + gyroskop_zout * elapsed_time


        accel_xout = read_word_2c(0x3b)
        accel_yout = read_word_2c(0x3d)
        accel_zout = read_word_2c(0x3f)

        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0


        roll = 0.96 * gyroskop_xout + 0.04 * get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        pitch = 0.96 * gyroskop_yout + 0.04 * get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

        print("yaw = {}, pitch={}, roll={}".format(yaw, pitch, roll))
    except:
        continue
