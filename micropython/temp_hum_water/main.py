from machine import Pin, SPI
from dht import DHT11
from ssd1306 import SSD1306_SPI
from time import sleep, sleep_ms
import onewire, ds18x20
import network
import urequests

HTTP_SERVER = "http://136.167.58.213:1880" # The IP address of the raspberry pi
HTTP_NODE = "/sensor"
RATE = 10  # How often do you want the update to be

dat = Pin(2)
d = DHT11(Pin(16))
ds = ds18x20.DS18X20(onewire.OneWire(dat))
roms = ds.scan()
ip = network.WLAN(network.STA_IF).ifconfig()[0]

spi = SPI(1, baudrate=8000000, polarity=0, phase=0)
oled = SSD1306_SPI(128,64, spi, res=Pin(4), dc=Pin(5), cs=Pin(15))


while True:
    oled.fill(0)
    oled.text(ip, 0, 0)
    d.measure()
    temp = 1.8*d.temperature()+32
    hum = d.humidity()
    oled.text("Temp: {} F".format(temp), 0, 20)
    oled.text("Hum: {}%".format(hum), 0, 30)
    ds.convert_temp()
    sleep_ms(750)
    water_temp = ""
    for rom in roms:
        water_temp += str(ds.read_temp(rom))
    water_temp = 1.8*round(float(water_temp), 1)+32
    oled.text("Water: {} F".format(water_temp), 0, 40)
    oled.show()

    data = {
        "temperature": temp,
        "humidity": hum,
        "water_temp": water_temp
    }
    
    try:
        r = urequests.post(HTTP_SERVER+HTTP_NODE, json=data)
    except:
        continue
    r.close()

    sleep(RATE)