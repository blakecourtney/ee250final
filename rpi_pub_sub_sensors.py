import os
import ssl
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
HOST=os.environ.get("MQTT_SERVER", "mqtt.jiahaokuang.com")
PORT=int(os.environ.get("MQTT_PORT", 1883))

tempsensor = 4
blue = 0
line = ""

#SSL/TLS CA
ca_cert = "/Documents/EE250/ee250final/public.key"

print("server:"+ HOST)
print("port:"+ str(PORT))

def init_lcd():
    setRGB(200, 200,200)
    setText("               \n               ")


def handle_temp(client, userdata, msg):
    temp_state = msg.payload.decode("UTF-8", 'strict')
    # Get the temp Ranger value
    print("temp: ", temp_state)
   # setText(temp_state)


def handle_target(client, userdata, msg):
    target_temperature = msg.payload.decode("UTF-8", 'strict')

def handle_hum(client, userdata, msg):
    hum_state = msg.payload.decode("UTF-8", 'strict')
    # Get the Ultrasonic Ranger value
    print("hum: ", hum_state)
    #setText(hum_state)


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe(USERNAME+"/thermostat/indoor/currentTemperature")  # add username are parameter
    client.subscribe(USERNAME+"/thermostat/indoor/currentHumidity")
    client.subscribe(USERNAME+"/thermostat/indoor/targetTemperature")

    #subscribe to topics of interest here
    # add callback functions
    client.message_callback_add(USERNAME+"/thermostat/indoor/currentTemperature", handle_temp)
    client.message_callback_add(USERNAME+"/thermostat/indoor/currentHumidity", handle_hum)
    client.message_callback_add(USERNAME+"/thermostat/indoor/targetTemperature", handle_target
)
    
#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


def get_dht(tempsensor):
    # Get the temp and hum value
    return grovepi.dht(tempsensor,blue)


if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()

    #enable ssl/tls
    client.tls_set(ca_certs=ca_cert, tls_version=ssl.PROTOCOL_TLSv1_1)

    client.on_message = on_message
    client.on_connect = on_connect
    init_lcd()
    client.connect(host=HOST, port=PORT, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)
        [temp,humidity] = get_dht(tempsensor)
        print("temp = %.02f C humidity =%.02f%%"%(temp, humidity))
        line = "temp = %.02f C \n humidity =%.02f%%"%(temp, humidity)
        setText_norefresh(line)
        client.publish(USERNAME+"/thermostat/indoor/currentTemperature", temp)
        client.publish(USERNAME+"/thermostat/indoor/currentHumidity", humidity)