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

sys.path.append("../../Software/Python/")
sys.path.append('../../Software/Python/grove_rgb_lcd')

import grovepi
from grove_rgb_lcd import *
import paho.mqtt.client as mqtt
import time

# obtain environment variables or default
USERNAME = os.environ.get("MQTT_USERNAME","NoMoreStruggle")
HOST=os.environ.get("MQTT_SERVER", "broker.emqx.io")
PORT=int(os.environ.get("MQTT_PORT", 1883))
ULTRASONIC_RANGER = 4
LED_PIN = 3
BUTTON_PIN=8

print("server:"+ HOST)
print("port:"+ str(PORT))

def init_lcd():
    setRGB(200, 200,200)
    setText("               \n               ")

def handel_lcd(client, userdata, msg):
    lcd_state = msg.payload.decode("UTF-8", 'strict')
    # Get the Ultrasonic Ranger value
    print("LCD: ", lcd_state)
    setText(lcd_state)

def handel_led(client, userdata, msg):
    led_state = msg.payload.decode("UTF-8", 'strict')
    print("LED: ", led_state)
    if led_state == "LED ON":
        grovepi.digitalWrite(LED_PIN, 1)
    elif led_state == "LED OFF":
        grovepi.digitalWrite(LED_PIN, 0)

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe(USERNAME+"/led")  # add username are parameter
    client.subscribe(USERNAME+"/lcd")
    #subscribe to topics of interest here
    # add callback functions
    client.message_callback_add(USERNAME+"/lcd", handel_lcd)
    client.message_callback_add(USERNAME+"/led", handel_led)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


def get_ultrasonic_ranger(ULTRASONIC_RANGER):
    # Get the Ultrasonic Ranger value
    return grovepi.ultrasonicRead(ULTRASONIC_RANGER)

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
        ul_range = get_ultrasonic_ranger(ULTRASONIC_RANGER)
        print("RPI: ", ul_range, "cm")
        client.publish(USERNAME+"/ultrasonicRanger", ul_range)
        if grovepi.digitalRead(BUTTON_PIN):
            print("Button pressed!")
            client.publish(USERNAME+"/button", "Button pressed!")