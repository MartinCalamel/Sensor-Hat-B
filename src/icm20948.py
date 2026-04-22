import time
import smbus2 as smbus
import struct

class ICM20948:
        def __init__(self):
                self.bus = smbus.SMBus(1)
                self.address = 0x68  # I2C address (AD0=GND)
                self._init_sensor()
        
        def _init_sensor(self):
                # Power Management 1: Clock source = Auto, disable sleep
                self.bus.write_byte_data(self.address, 0x06, 0x01)
                time.sleep(0.1)
                # Accelerometer Configuration: ±2g, ACCEL_DLPF_CFG=3 (44Hz)
                self.bus.write_byte_data(self.address, 0x14, 0x03)
                # Gyroscope Configuration: ±250°/s, GYRO_DLPF_CFG=3 (41Hz)
                self.bus.write_byte_data(self.address, 0x13, 0x03)
                time.sleep(0.1)
        
        def read(self):
                # Read accelerometer (6 bytes from 0x2D)
                accel_data = self.bus.read_i2c_block_data(self.address, 0x2D, 6)
                # Read gyroscope (6 bytes from 0x33)
                gyro_data = self.bus.read_i2c_block_data(self.address, 0x33, 6)
                return accel_data + gyro_data
        
        def read_accel_gyro(self):
                # Read accelerometer (6 bytes from 0x2D)
                accel_data = self.bus.read_i2c_block_data(self.address, 0x2D, 6)
                # Read gyroscope (6 bytes from 0x33)
                gyro_data = self.bus.read_i2c_block_data(self.address, 0x33, 6)
                
                # Convert to signed 16-bit integers (big-endian)
                accel_x = struct.unpack('>h', bytes([accel_data[0], accel_data[1]]))[0] / 16384.0 * 2 * 9.81
                accel_y = struct.unpack('>h', bytes([accel_data[2], accel_data[3]]))[0] / 16384.0 * 2 * 9.81
                accel_z = struct.unpack('>h', bytes([accel_data[4], accel_data[5]]))[0] / 16384.0 * 2 * 9.81
                
                gyro_x = struct.unpack('>h', bytes([gyro_data[0], gyro_data[1]]))[0] / 131.0
                gyro_y = struct.unpack('>h', bytes([gyro_data[2], gyro_data[3]]))[0] / 131.0
                gyro_z = struct.unpack('>h', bytes([gyro_data[4], gyro_data[5]]))[0] / 131.0
                
                return (round(accel_x, 2), round(accel_y, 2), round(accel_z, 2)), (round(gyro_x, 2), round(gyro_y, 2), round(gyro_z, 2))

if __name__ == "__main__":
        sensor = ICM20948()
        accel, gyro = sensor.read_accel_gyro()
        print(f"Accel: {accel}, Gyro: {gyro}")
