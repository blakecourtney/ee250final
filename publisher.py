# EE 250L Lab 05: MQTT

# Haily Kuang
# Blake Courtney
#
# Github repo:
# https://github.com/usc-ee250-fall2024/mqtt-no-more-struggle

"""EE 250L Lab 04 Starter Code

Run vm_publisher.py in a separate terminal on your VM."""

import os
import paho.mqtt.client as mqtt
import time
from pynput import keyboard

# obtain environment variables or default
USERNAME = os.environ.get("MQTT_USERNAME", "NoMoreStruggle")
HOST = os.environ.get("MQTT_SERVER", "broker.emqx.io")
PORT = int(os.environ.get("MQTT_PORT", 1883))

print("server:" + HOST)
print("port:" + str(PORT))


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code " + str(rc))

    # subscribe to topics of interest here


# Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


def on_press(key):
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys

    if k == 'w':
        print("w")
        # send "w" character to rpi
        client.publish(USERNAME + "/lcd", "w")
    elif k == 'a':
        print("a")
        # send "a" character to rpi
        client.publish(USERNAME + "/lcd", "a")
        # send "LED_ON"
        client.publish(USERNAME + "/led", "LED ON")
    elif k == 's':
        print("s")
        # send "s" character to rpi
        client.publish(USERNAME + "/lcd", "s")
    elif k == 'd':
        print("d")
        # send "d" character to rpi
        client.publish(USERNAME + "/lcd", "d")
        # send "LED_OFF"
        client.publish(USERNAME + "/led", "LED OFF")


if __name__ == '__main__':
    # setup the keyboard event listener
    lis = keyboard.Listener(on_press=on_press)
    lis.start()  # start to listen on a separate thread

    # this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host=HOST, port=PORT, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)


