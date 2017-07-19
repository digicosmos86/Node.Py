from machine import ADC
from time import sleep

adc = ADC(0)

while True:
    adc.read()
    sleep(1)


from machine import Pin
from time import sleep
p5 = Pin(5, Pin.IN)

while True:
    p5.value()
    sleep(1)