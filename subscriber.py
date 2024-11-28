# EE 250L Lab 05: MQTT

# Haily Kuang
# Blake Courtney
#
# Github repo:
# https://github.com/usc-ee250-fall2024/mqtt-no-more-struggle

"""EE 250L Lab 04 Starter Code

Run vm_subscriber.py in a separate terminal on your VM."""
import os
import paho.mqtt.client as mqtt
import time
import sys
#import RPi.GPIO as GPIO
#import grovepi
import time
import math
sys.path.append('~/Software/Python/')
sys.path.append('~/Software/Python/grove_rgb_lcd')
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
#from grove_rgb_lcd import *


# obtain environment variables or default
USERNAME = os.environ.get("MQTT_USERNAME", "NoMoreStruggle")
HOST=os.environ.get("MQTT_SERVER", "broker.emqx.io")
PORT=int(os.environ.get("MQTT_PORT", 1883))

print("server:"+ HOST)
print("port:"+ str(PORT))

def handle_temp(client, userdata, msg):
    temp_state = msg.payload.decode("UTF-8", 'strict')
    # Get the temp Ranger value
    print("temp: ", temp_state)


def handle_hum(client, userdata, msg):
    hum_state = msg.payload.decode("UTF-8", 'strict')
    # Get the Ultrasonic Ranger value
    print("hum: ", hum_state)

def on_connect(client, userdata, flags, rc):
    #subscribe to the ultrasonic ranger topic here
    if rc == 0:
        print("Connected to server (i.e., broker) with result code "+str(rc))
        # add username are parameter
        # add callback functions
        client.message_callback_add(USERNAME+"/temp", handle_temp)
        client.message_callback_add(USERNAME+"/hum", handle_hum)

        #subscribe to topics of interest
        client.subscribe(USERNAME+"/temp")
        client.subscribe(USERNAME+"/hum")
    else:
        print("Failed to connect to server, return code %d\n", str(rc))

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host=HOST, port=PORT, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)
