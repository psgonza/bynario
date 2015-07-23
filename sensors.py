#!/usr/bin/env python
import Adafruit_BMP.BMP085 as BMP085
from datetime import datetime
import time
import sys
import os
import glob


sensor_int = BMP085.BMP085()
sensor_int = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


while True:
    temperature = sensor_int.read_temperature()
    pressure = sensor_int.read_pressure()
    to_print=str(datetime.now().strftime('%Y-%m-%d %H:%M'))+","+ str(temperature)+","+ str(pressure / 100.) + "," + str(read_temp()) + "\n"
    logF = open("/usr/share/nginx/www/temperatures.csv",'a')
    logF.write(to_print)
    logF.close()
    time.sleep(300)

    
