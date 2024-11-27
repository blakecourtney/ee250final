import sys
import smbus
import RPi.GPIO as GPIO

sys.path.append('~/Software/Python/')
sys.path.append('~/Software/Python/grove_rgb_lcd')
sys.path.append('~/Software/Python/grove_i2c_temp_hum_sensor_mini')

import time
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`

import grovepi
from grove_rgb_lcd import *
from grove_i2c_temp_hum_mini.py import *
from grove_i2c_temp_hum_mini.py import grove_i2c_temp_hum_mini.py
#from grove_i2c_temp_hum_hdc1000 import *
#from grove_i2c_temp_hum_hdc1000 import HDC1000

import grove_i2c_temp_hum_mini
import time

#hdc = HDC1000()
#hdc.Config()

t= grove_i2c_temp_hum_mini.th02()

#clear lcd
setText("TESTING")
line1 = ""

while True:
    try:
        #read distance from ultrasonic
        #read potentiometer threshold
        #temp = hdc.Temperature()
        #hum = hdc.Humidity()
        #format text

        line1 = "Temp: %.2fC\tHumidity:%.2f" % (t.getTemperature(), t.getHumidity()), "%"
        setText_norefresh(line1)

    except IOError:
        print("Error")