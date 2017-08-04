from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(sda=Pin(4), scl=Pin(5))

oled = SSD1306_I2C(128, 64, i2c)
oled.text("Hello world!", 0, 30)
oled.show()