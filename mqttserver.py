# EE 250L Lab 05: MQTT

# Haily Kuang
# Blake Courtney
#
# Github repo:
# https://github.com/usc-ee250-fall2024/mqtt-no-more-struggle

"""EE 250L Lab 04 Starter Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import os
import sys
import smbus
import RPi.GPIO as GPIO
import math
import grovepi
from grove_rgb_lcd import *
import paho.mqtt.client as mqtt
import time
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('~/Software/Python/')
sys.path.append('~/Software/Python/grove_rgb_lcd')



# obtain environment variables or default
USERNAME = os.environ.get("MQTT_USERNAME","NoMoreStruggle")
HOST=os.environ.get("MQTT_SERVER", "broker.emqx.io")
PORT=int(os.environ.get("MQTT_PORT", 1883))

tempsensor = 4
blue = 0
print("server:"+ HOST)
print("port:"+ str(PORT))

def init_lcd():
    setRGB(200, 200,200)
    setText("               \n               ")


def handle_temp(client, userdata, msg):
    temp_state = msg.payload.decode("UTF-8", 'strict')
    # Get the temp Ranger value
    print("temp: ", temp_state)
    setText(temp_state)


def handle_hum(client, userdata, msg):
    hum_state = msg.payload.decode("UTF-8", 'strict')
    # Get the Ultrasonic Ranger value
    print("hum: ", hum_state)
    setText(hum_state)


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe(USERNAME+"/temp")  # add username are parameter
    client.subscribe(USERNAME+"/hum")
    #subscribe to topics of interest here
    # add callback functions
    client.message_callback_add(USERNAME+"/temp", handle_temp)
    client.message_callback_add(USERNAME+"/hum", handle_hum)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


def get_dht(tempsensor):
    # Get the temp and hum value
    return grovepi.dht(tempsensor,blue)


if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    init_lcd()
    client.connect(host=HOST, port=PORT, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)
        [temp,humidity] = get_dht(tempsensor)
        print("temp = %.02f C humidity =%.02f%%"%(temp, humidity))
        client.publish(USERNAME+"/temp", temp)
        client.publish(USERNAME+"/hum", humidity)