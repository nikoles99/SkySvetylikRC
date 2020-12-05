import math

import smbus


class MPU6050:
    # Global Variables
    GRAVITIY_MS2 = 9.80665
    address = None
    bus = smbus.SMBus(1)

    # Scale Modifiers
    ACCEL_SCALE_MODIFIER_2G = 16384.0
    ACCEL_SCALE_MODIFIER_4G = 8192.0
    ACCEL_SCALE_MODIFIER_8G = 4096.0
    ACCEL_SCALE_MODIFIER_16G = 2048.0

    GYRO_SCALE_MODIFIER_250DEG = 131.0
    GYRO_SCALE_MODIFIER_500DEG = 65.5
    GYRO_SCALE_MODIFIER_1000DEG = 32.8
    GYRO_SCALE_MODIFIER_2000DEG = 16.4

    # Pre-defined ranges
    ACCEL_RANGE_2G = 0x00
    ACCEL_RANGE_4G = 0x08
    ACCEL_RANGE_8G = 0x10
    ACCEL_RANGE_16G = 0x18

    GYRO_RANGE_250DEG = 0x00
    GYRO_RANGE_500DEG = 0x08
    GYRO_RANGE_1000DEG = 0x10
    GYRO_RANGE_2000DEG = 0x18

    # MPU-6050 Registers
    PWR_MGMT_1 = 0x6B
    PWR_MGMT_2 = 0x6C

    SELF_TEST_X = 0x0D
    SELF_TEST_Y = 0x0E
    SELF_TEST_Z = 0x0F
    SELF_TEST_A = 0x10

    ACCEL_XOUT0 = 0x3B
    ACCEL_XOUT1 = 0x3C
    ACCEL_YOUT0 = 0x3D
    ACCEL_YOUT1 = 0x3E
    ACCEL_ZOUT0 = 0x3F
    ACCEL_ZOUT1 = 0x40

    TEMP_OUT0 = 0x41
    TEMP_OUT1 = 0x42

    GYRO_XOUT0 = 0x43
    GYRO_XOUT1 = 0x44
    GYRO_YOUT0 = 0x45
    GYRO_YOUT1 = 0x46
    GYRO_ZOUT0 = 0x47
    GYRO_ZOUT1 = 0x48

    ACCEL_CONFIG = 0x1C
    GYRO_CONFIG = 0x1B
    gyro_x_error = 0
    gyro_y_error = 0
    gyro_z_error = 0
    accel_x_error = 0
    accel_y_error = 0

    angle_roll = 0
    angle_pitch = 0
    angle_yaw = 0
    first_reading = True

    def __init__(self, address=0x68):
        self.address = address

        # Wake up the MPU-6050 since it starts in sleep mode
        self.bus.write_byte_data(self.address, self.PWR_MGMT_1, 0x00)
        self.set_accel_range(self.ACCEL_RANGE_8G)
        self.set_gyro_range(self.GYRO_RANGE_500DEG)
        self.calibrate()

    # I2C communication methods

    def read_i2c_word(self, register):
        """Read two i2c registers and combine them.
        register -- the first register to read from.
        Returns the combined read results.
        """
        # Read the data from the registers
        value = 0
        is_error_thrown = True
        while is_error_thrown:
            try:
                high = self.bus.read_byte_data(self.address, register)
                low = self.bus.read_byte_data(self.address, register + 1)

                value = (high << 8) + low
                if (value >= 0x8000):
                    value = -((65535 - value) + 1)
                is_error_thrown = False
            except:
                is_error_thrown = True

        return value

        # MPU-6050 Methods

    def get_temp(self):
        """Reads the temperature from the onboard temperature sensor of the MPU-6050.
        Returns the temperature in degrees Celcius.
        """
        # Get the raw data
        raw_temp = self.read_i2c_word(self.TEMP_OUT0)

        # Get the actual temperature using the formule given in the
        # MPU-6050 Register Map and Descriptions revision 4.2, page 30
        actual_temp = (raw_temp / 340) + 36.53

        # Return the temperature
        return actual_temp

    def set_accel_range(self, accel_range):
        """Sets the range of the accelerometer to range.
        accel_range -- the range to set the accelerometer to. Using a
        pre-defined range is advised.
        """
        # First change it to 0x00 to make sure we write the correct value later
        self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, 0x00)

        # Write the new range to the ACCEL_CONFIG register
        self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, accel_range)

    def read_accel_range(self, raw=False):
        """Reads the range the accelerometer is set to.
        If raw is True, it will return the raw value from the ACCEL_CONFIG
        register
        If raw is False, it will return an integer: -1, 2, 4, 8 or 16. When it
        returns -1 something went wrong.
        """
        # Get the raw value
        raw_data = self.bus.read_byte_data(self.address, self.ACCEL_CONFIG)

        if raw is True:
            return raw_data
        elif raw is False:
            if raw_data == self.ACCEL_RANGE_2G:
                return 2
            elif raw_data == self.ACCEL_RANGE_4G:
                return 4
            elif raw_data == self.ACCEL_RANGE_8G:
                return 8
            elif raw_data == self.ACCEL_RANGE_16G:
                return 16
            else:
                return -1

    def get_accel_data(self, g=False):
        """Gets and returns the X, Y and Z values from the accelerometer.
        If g is True, it will return the data in g
        If g is False, it will return the data in m/s^2
        Returns a dictionary with the measurement results.
        """
        # Read the data from the MPU-6050
        x = self.read_i2c_word(self.ACCEL_XOUT0)
        y = self.read_i2c_word(self.ACCEL_YOUT0)
        z = self.read_i2c_word(self.ACCEL_ZOUT0)

        accel_scale_modifier = None
        accel_range = self.read_accel_range(True)

        if accel_range == self.ACCEL_RANGE_2G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G
        elif accel_range == self.ACCEL_RANGE_4G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_4G
        elif accel_range == self.ACCEL_RANGE_8G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_8G
        elif accel_range == self.ACCEL_RANGE_16G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_16G
        else:
            print("Unkown range - accel_scale_modifier set to self.ACCEL_SCALE_MODIFIER_2G")
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G

        x = x / accel_scale_modifier
        y = y / accel_scale_modifier
        z = z / accel_scale_modifier

        if g is True:
            return x, y, z
        elif g is False:
            x = x * self.GRAVITIY_MS2
            y = y * self.GRAVITIY_MS2
            z = z * self.GRAVITIY_MS2
            return x, y, z

    def set_gyro_range(self, gyro_range):
        """Sets the range of the gyroscope to range.
        gyro_range -- the range to set the gyroscope to. Using a pre-defined
        range is advised.
        """
        # First change it to 0x00 to make sure we write the correct value later
        self.bus.write_byte_data(self.address, self.GYRO_CONFIG, 0x00)

        # Write the new range to the ACCEL_CONFIG register
        self.bus.write_byte_data(self.address, self.GYRO_CONFIG, gyro_range)

    def read_gyro_range(self, raw=False):
        """Reads the range the gyroscope is set to.
        If raw is True, it will return the raw value from the GYRO_CONFIG
        register.
        If raw is False, it will return 250, 500, 1000, 2000 or -1. If the
        returned value is equal to -1 something went wrong.
        """
        # Get the raw value
        raw_data = self.bus.read_byte_data(self.address, self.GYRO_CONFIG)

        if raw is True:
            return raw_data
        elif raw is False:
            if raw_data == self.GYRO_RANGE_250DEG:
                return 250
            elif raw_data == self.GYRO_RANGE_500DEG:
                return 500
            elif raw_data == self.GYRO_RANGE_1000DEG:
                return 1000
            elif raw_data == self.GYRO_RANGE_2000DEG:
                return 2000
            else:
                return -1

    def get_gyro_data(self):
        """Gets and returns the X, Y and Z values from the gyroscope.
        Returns the read values in a dictionary.
        """
        # Read the raw data from the MPU-6050
        x = self.read_i2c_word(self.GYRO_XOUT0)
        y = self.read_i2c_word(self.GYRO_YOUT0)
        z = self.read_i2c_word(self.GYRO_ZOUT0)

        gyro_scale_modifier = None
        gyro_range = self.read_gyro_range(True)

        if gyro_range == self.GYRO_RANGE_250DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG
        elif gyro_range == self.GYRO_RANGE_500DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_500DEG
        elif gyro_range == self.GYRO_RANGE_1000DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_1000DEG
        elif gyro_range == self.GYRO_RANGE_2000DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_2000DEG
        else:
            print("Unkown range - gyro_scale_modifier set to self.GYRO_SCALE_MODIFIER_250DEG")
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG

        x = x / gyro_scale_modifier
        y = y / gyro_scale_modifier
        z = z / gyro_scale_modifier

        return {'x': x, 'y': y, 'z': z}

    def calibrate(self):
        accel_x_sum = 0
        accel_y_sum = 0
        gyro_x_sum = 0
        gyro_y_sum = 0
        gyro_z_sum = 0
        CALIBRATION_RANGE = 200

        for i in range(CALIBRATION_RANGE):
            accel_xout = self.read_i2c_word(self.ACCEL_XOUT0) / self.ACCEL_SCALE_MODIFIER_2G
            accel_yout = self.read_i2c_word(self.ACCEL_YOUT0) / self.ACCEL_SCALE_MODIFIER_2G
            accel_zout = self.read_i2c_word(self.ACCEL_ZOUT0) / self.ACCEL_SCALE_MODIFIER_2G
            accel_x_sum = accel_x_sum + self.get_x_rotation(accel_xout, accel_yout, accel_zout)
            accel_y_sum = accel_y_sum + self.get_y_rotation(accel_xout, accel_yout, accel_zout)
            gyro_x_sum = gyro_x_sum + self.read_i2c_word(self.GYRO_XOUT0)
            gyro_y_sum = gyro_y_sum + self.read_i2c_word(self.GYRO_YOUT0)
            gyro_z_sum = gyro_z_sum + self.read_i2c_word(self.GYRO_ZOUT0)

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

    def get_yaw_pitch_roll_angles(self):
        #gyro_x_out = (self.read_i2c_word(self.GYRO_XOUT0) - self.gyro_x_error) * 0.00012195
        #gyro_y_out = (self.read_i2c_word(self.GYRO_YOUT0) - self.gyro_y_error) * 0.00012195
        #gyro_z_out = (self.read_i2c_word(self.GYRO_ZOUT0) - self.gyro_z_error) * 0.00012195
        #self.angle_pitch += self.angle_roll * math.sin(gyro_z_out * 0.00000213)
        #self.angle_roll -= self.angle_pitch * math.sin(gyro_z_out * 0.00000213)

        gyro_x_out = (self.read_i2c_word(self.GYRO_XOUT0) - self.gyro_x_error) * 0.0000611
        gyro_y_out = (self.read_i2c_word(self.GYRO_YOUT0) - self.gyro_y_error) * 0.0000611
        gyro_z_out = (self.read_i2c_word(self.GYRO_ZOUT0) - self.gyro_z_error) * 0.0000611

        self.angle_roll = self.angle_roll + gyro_x_out
        self.angle_pitch = self.angle_pitch + gyro_y_out
        self.angle_yaw = self.angle_yaw + gyro_z_out

        sin = math.sin(gyro_z_out * 0.000001066)
        self.angle_roll += self.angle_pitch * sin
        self.angle_pitch -= self.angle_roll * sin

        accel_x_out, accel_y_out, accel_z_out = self.get_accel_data()
        accel_x = self.get_x_rotation(accel_x_out, accel_y_out, accel_z_out) - self.accel_x_error
        accel_y = self.get_y_rotation(accel_x_out, accel_y_out, accel_z_out) - self.accel_y_error

        if not self.first_reading:
            self.angle_roll = self.angle_roll * 0.96 + accel_x * 0.04
            self.angle_pitch = self.angle_pitch * 0.96 + accel_y * 0.04
        else:
            self.angle_roll = accel_x
            self.angle_pitch = accel_y
            self.first_reading = False
        return self.angle_yaw, self.angle_roll, self.angle_pitch


mpu_ = MPU6050()
while True:
    yaw, roll, pitch = mpu_.get_yaw_pitch_roll_angles()
    print("yaw = {}, roll={}, pitch={}".format(yaw, roll, pitch))
