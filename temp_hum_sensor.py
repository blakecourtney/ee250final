import sys
import smbus
import RPi.GPIO as GPIO

sys.path.append('~/Software/Python/')
sys.path.append('~/Software/Python/grove_rgb_lcd')
sys.path.append('~/Software/Python/grove_i2c_temp_hum_hdc1000')

import time
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`

import grovepi
from grove_rgb_lcd import *
from grove_i2c_temp_hum_hdc1000 import *
from grove_i2c_temp_hum_hdc1000 import HDC1000

hdc = HDC1000()
hdc.Config()

#clear lcd
setText("TESTING")
line1 = ""

while True:
    try:
        #read distance from ultrasonic
        #read potentiometer threshold
        temp = hdc.Temperature()
        hum = hdc.Humidity()
        #format text
        print('Temp    : %.2f C' % hdc.Temperature())
        print('Humidity: %.2f %%' % hdc.Humidity())

        line1 = 'Temp    : %.2f C' % str(temp) + '\n' + 'Humidity: %.2f %%' % str(hum)
        setText_norefresh(line1)

    except IOError:
        print("Error")