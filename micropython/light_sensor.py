from machine import Pin, I2C
#from tsl2561 import TSL2561

i2c = I2C(scl=Pin(5), sda=Pin(4))
i2c.init(scl=Pin(5), sda=Pin(4))
i2c.start()