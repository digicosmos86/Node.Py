from machine import Pin, SPI
import ssd1306

spi = SPI(-1,baudrate=8000000, phase=0, polarity=0)

oled = ssd1306.SSD1306_SPI(128,64, spi, res=Pin(4), dc=Pin(5), cs=Pin(15))
oled.fill(0)
oled.show()