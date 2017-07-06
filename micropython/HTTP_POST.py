####################
# initialization
####################

HTTP_SERVER = "http://10.20.245.116:1880" # The IP address of the raspberry pi
HTTP_NODE = "/sensor"
RATE = 10  # How often do you want the update to be
PIN = 5    # The pin number the sensor is connected to

import machine
import urequests
from dht import DHT11
from time import sleep

d = DHT11(machine.Pin(PIN))

while True:
    d.measure()
    temp = d.temperature()
    hum = d.humidity()
    temp_hum = {
        "temperature": temp,
        "humidity": hum
    }
    
    r = urequests.post(url = HTTP_SERVER+HTTP_NODE, json = temp_hum)
    r.close()
    sleep(RATE)