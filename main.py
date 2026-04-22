from src.icm20948 import ICM20948
from src.lps22hb import LPS22HB
from src.shtc3_working import SHTC3

import time
import signal

def stop():
    global running
    print("Server shutting down...")
    running = False

running = True
signal.signal(signal.SIGINT, stop)

sensor_1 = SHTC3()
sensor_2 = LPS22HB()
sensor_3 = ICM20948()

def main():
    while running:
        temp, humidity = sensor_1.read_temperature_humidity()
        press, temp2 = sensor_2.read_pressure_temperature()
        accel, gyro = sensor_3.read_accel_gyro()
        
        print(f"\033[H\033[J", end="")
        print(f"SHTC3:    {temp}°C  {humidity}%")
        print(f"LPS22HB:  {press}hPa  {temp2}°C")
        print(f"ICM-20948: A{accel} G{gyro}")
        
        time.sleep(0.5)