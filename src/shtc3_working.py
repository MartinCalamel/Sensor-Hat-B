import time
import smbus2 as smbus
from smbus2 import i2c_msg
class SHTC3:
        def __init__(self):
                self.bus = smbus.SMBus(1)
                self.address = 0x70
        def send(self, data:bytes):
                self.bus.write_i2c_block_data(self.address, data[0], data[1:])
                time.sleep(0.01)
        def sleep(self):
                self.send(bytes([0xB0, 0x98]))
        def wakeup(self):
                self.send(bytes([0x35, 0x17]))
                time.sleep(0.1)
        def measurement(self):
                self.send(bytes([0x5C, 0x24]))
                time.sleep(0.02)
        def read(self):
                self.wakeup()
                self.measurement()
                msg = i2c_msg.read(self.address, 6)
                self.bus.i2c_rdwr(msg)
                block = list(msg)
                self.sleep()
                return block
        def read_temperature_humidity(self):
                block = self.read()
                rh_raw = (block[0] << 8) | block[1]
                temp_raw = (block[3] << 8) | block[4]
                temperature = (temp_raw / 65536.0) * 175 - 45
                humidity = (rh_raw / 65536.0) * 100
                return round(temperature, 2), round(humidity, 2)
if __name__ == "__main__":
        sensor = SHTC3()
        temp, humidity = sensor.read_temperature_humidity()
        print(f"Temperature: {temp}°C, Humidity: {humidity}%")
