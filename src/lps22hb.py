import time
import smbus2 as smbus

class LPS22HB:
        def __init__(self):
                self.bus = smbus.SMBus(1)
                self.address = 0x5C  # I2C address (SDO connected to GND)
                self._init_sensor()
        
        def _init_sensor(self):
                # CTRL_REG1: Enable sensor, ODR=25Hz, BDU=1
                self.bus.write_byte_data(self.address, 0x10, 0x70)
                time.sleep(0.1)
        
        def read(self):
                # Read pressure (3 bytes, little-endian from 0x28)
                press_xl = self.bus.read_byte_data(self.address, 0x28)
                press_l = self.bus.read_byte_data(self.address, 0x29)
                press_h = self.bus.read_byte_data(self.address, 0x2A)
                pressure_raw = (press_h << 16) | (press_l << 8) | press_xl
                
                # Read temperature (2 bytes, little-endian from 0x2B)
                temp_l = self.bus.read_byte_data(self.address, 0x2B)
                temp_h = self.bus.read_byte_data(self.address, 0x2C)
                temp_raw = (temp_h << 8) | temp_l
                
                # Convert to signed integers
                if temp_raw & 0x8000:
                        temp_raw = temp_raw - 0x10000
                
                return [press_xl, press_l, press_h, temp_l, temp_h]
        
        def read_pressure_temperature(self):
                # Read pressure (3 bytes)
                press_xl = self.bus.read_byte_data(self.address, 0x28)
                press_l = self.bus.read_byte_data(self.address, 0x29)
                press_h = self.bus.read_byte_data(self.address, 0x2A)
                pressure_raw = (press_h << 16) | (press_l << 8) | press_xl
                
                # Read temperature (2 bytes)
                temp_l = self.bus.read_byte_data(self.address, 0x2B)
                temp_h = self.bus.read_byte_data(self.address, 0x2C)
                temp_raw = (temp_h << 8) | temp_l
                
                # Convert to signed integer
                if temp_raw & 0x8000:
                        temp_raw = temp_raw - 0x10000
                
                # Convert to actual values
                pressure = pressure_raw / 4096.0  # 4096 LSB/hPa
                temperature = temp_raw / 100.0    # 100 LSB/°C
                
                return round(pressure, 2), round(temperature, 2)

if __name__ == "__main__":
        sensor = LPS22HB()
        pressure, temperature = sensor.read_pressure_temperature()
        print(f"Pressure: {pressure}hPa, Temperature: {temperature}°C")
