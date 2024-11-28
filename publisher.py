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


if __name__ == '__main__':
    # this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host=HOST, port=PORT, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)


