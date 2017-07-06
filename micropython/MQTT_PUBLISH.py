####################
# initialization
####################

MQTT_SERVER = "192.168.1.77" # The IP address of the MQTT Broker/Raspberry Pi
MQTT_PORT = 1883             # The Port number of the broker, usually 1883
TOPIC = "/sensor1/readings"  # Choose a topic that only you can subscribe
RATE = 10  # How often do you want the update to be
PIN = 5    # The pin number the sensor is connected to

import machine
import json
from dht import DHT11
from time import sleep
from umqtt.simple import MQTTClient

d = DHT11(machine.Pin(PIN))

mqtt = MQTTClient("umqtt-client", server = MQTT_SERVER, port= MQTT_PORT)
mqtt.connect(clean_session = False)

while True:
    d.measure()
    temp = d.temperature()
    hum = d.humidity()
    temp_hum = {
        "temperature": temp,
        "humidity": hum
    }
    
    mqtt.publish(TOPIC, json.dumps(temp_hum))
    sleep(RATE)