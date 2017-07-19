from machine import Pin, SPI
from ssd1306 import SSD1306_SPI

spi = SPI(1, baudrate = 100000, polarity = 1, phase = 0)
oled = SSD1306_SPI(128, 64, spi, dc = Pin(5), res = Pin(4), cs = Pin(15))
oled.fill(0)
oled.show()