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


# obtain environment variables or default
USERNAME = os.environ.get("MQTT_USERNAME", "NoMoreStruggle")
HOST=os.environ.get("MQTT_SERVER", "broker.emqx.io")
PORT=int(os.environ.get("MQTT_PORT", 1883))

print("server:"+ HOST)
print("port:"+ str(PORT))

def handel_ultrasonic(client, userdata, msg):
    rpi_range = msg.payload.decode("UTF-8", 'strict')
    print("VM: ", rpi_range, "cm")

def handle_button(client, userdata, msg):
    button_state = msg.payload.decode("UTF-8", 'strict')
    print(button_state)

def on_connect(client, userdata, flags, rc):
    #subscribe to the ultrasonic ranger topic here
    if rc == 0:
        print("Connected to server (i.e., broker) with result code "+str(rc))
        # add username are parameter
        # add callback functions
        client.message_callback_add(USERNAME+"/ultrasonicRanger", handel_ultrasonic)
        client.message_callback_add(USERNAME+"/button", handle_button)

        #subscribe to topics of interest
        client.subscribe(USERNAME+"/button")
        client.subscribe(USERNAME+"/ultrasonicRanger")
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
