import ssd1306
from machine import I2C,delay
import math

x =xh = None
y = yh=None

i2c = I2C(0,I2C.MASTER,baudrate=400000)
oled=ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.pixel(64,32,1)
for _E8_A7_92_E5_BA_A6 in range(361):
  x = 30 * math.cos(_E8_A7_92_E5_BA_A6 / 180.0 * math.pi)
  y = 30 * math.sin(_E8_A7_92_E5_BA_A6 / 180.0 * math.pi)
  oled.pixel(int(64-x),int(32-y),1)
  
for i in range (0,361,30) :
    xh = 12 * math.cos(i/ 180.0 * math.pi)
    yh = 12 * math.sin(i/ 180.0 * math.pi)
    for j in range (0,361,10) :
        x = 18 * math.cos(j/ 180.0 * math.pi)
        y = 18 * math.sin(j/ 180.0 * math.pi)
        oled.line(64,32,int(64-x),int(32-y),1)
        oled.line(64,32,int(64-xh),int(32-yh),1)
        oled.show()
        delay(10)
        oled.line(64,32,int(64-x),int(32-y),0)
        oled.show()
	oled.line(64,32,int(64-xh),int(32-yh),0)
	oled.show()
	
