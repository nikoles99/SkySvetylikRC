import math

import smbus

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

bus = smbus.SMBus(1)  # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68


bus.write_byte_data(address, 0x19, 7)
bus.write_byte_data(address, 0x6B, 1)
bus.write_byte_data(address, 0x1A, 0)
bus.write_byte_data(address, 0x1B, 24)
bus.write_byte_data(address, 0x38, 1)
# time.sleep(1)


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


angle_pitch = 0
angle_roll = 0
angle_yaw = 0
first = True


def calibrate():
    accel_x_sum = 0
    accel_y_sum = 0
    accel_z_sum = 0
    gyro_x_sum = 0
    gyro_y_sum = 0
    gyro_z_sum = 0
    for i in range(200):
        try:
            accel_xout = read_word_2c(0x3b) / 16384.0
            accel_yout = read_word_2c(0x3d) / 16384.0
            accel_zout = read_word_2c(0x3f) / 16384.0
            accel_x_sum = accel_x_sum + get_x_rotation(accel_xout, accel_yout, accel_zout)
            accel_y_sum = accel_y_sum + get_y_rotation(accel_xout, accel_yout, accel_zout)
        except:
            continue
    accel_x_sum = accel_x_sum / 200
    accel_y_sum = accel_y_sum / 200

    for i in range(200):
        try:
            gyro_x_sum = gyro_x_sum + read_word_2c(0x43)
            gyro_y_sum = gyro_y_sum + read_word_2c(0x45)
            gyro_z_sum = gyro_z_sum + read_word_2c(0x47)
        except:
            continue
    gyro_x_sum = gyro_x_sum / 200
    gyro_y_sum = gyro_y_sum / 200
    gyro_z_sum = gyro_z_sum / 200

    return gyro_x_sum, gyro_y_sum, gyro_z_sum, accel_x_sum, accel_y_sum


gyro_x_sum, gyro_y_sum, gyro_z_sum, accel_x_sum, accel_y_sum = calibrate()


while True:
    try:
        gyroskop_xout = (read_word_2c(0x43) - gyro_x_sum) * 0.00012195
        gyroskop_yout = (read_word_2c(0x45) - gyro_y_sum) * 0.00012195
        gyroskop_zout = (read_word_2c(0x47) - gyro_z_sum) * 0.00012195

        angle_pitch = angle_pitch + gyroskop_xout
        angle_roll = angle_roll + gyroskop_yout
        angle_yaw = angle_yaw + gyroskop_zout

        angle_pitch += angle_roll * math.sin(gyroskop_zout * 0.00000213)
        angle_roll -= angle_pitch * math.sin(gyroskop_zout * 0.00000213)

        accel_xout = read_word_2c(0x3b)
        accel_yout = read_word_2c(0x3d)
        accel_zout = read_word_2c(0x3f)

        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0

        accel_x = get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled) - accel_x_sum
        accel_y = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled) - accel_y_sum

        if not first:
            angle_pitch = angle_pitch * 0.96 + accel_x * 0.04
            angle_roll = angle_roll * 0.96 + accel_y * 0.04
        else:
            angle_pitch = accel_x
            angle_roll = accel_y
            first = False

        print("yaw = {}, pitch={}, roll={}".format(angle_yaw, angle_pitch, angle_roll))
    except:
        continue
