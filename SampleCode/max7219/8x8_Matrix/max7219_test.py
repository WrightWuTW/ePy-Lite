import max7219
from machine import Pin, SPI
import utime

spi=SPI(sck=Pin.board.CLK0,miso=Pin.board.MISO, mosi=Pin.board.MOSI)

ss = Pin(Pin.board.P9, Pin.OUT)
display = max7219.Matrix8x8(spi, ss, 5) #creat virtual disaply five 8x8 matrixs  

while True:
    display.text('54321',0,0,1)
    display.show()


    for i in range(41):
        display.scroll(1,0)
        display.show()
        utime.sleep_ms(200)

"""
display.fill(0)
display.show()

display.pixel(0,0,1)
display.pixel(1,1,1)
display.hline(0,4,8,1)
display.vline(4,0,8,1)
display.line(8, 0, 16, 8, 1)
display.rect(17,1,6,6,1)
display.fill_rect(25,1,6,6,1)
display.show()

display.fill(0)
display.text('dead',0,0,1)
display.text('beef',32,0,1)
display.show()

display.fill(0)
display.text('12345678',0,0,1)
display.show()
display.scroll(-8,0) # 23456788
display.scroll(-8,0) # 34567888
display.show()
"""
