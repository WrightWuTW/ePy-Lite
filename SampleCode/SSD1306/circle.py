import ssd1306
from machine import I2C,delay
import math

_E8_A7_92_E5_BA_A6 = None
x = None
y = None


i2c = I2C(0,I2C.MASTER)
oled=ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0) #清除畫布
oled.pixel(64,32,1) # 圓心 (64,32)一點

''' 使用三角函數劃出一個圓'''
for i range(361):
  x = 30 * math.cos(i / 180.0 * math.pi)
  y = 30 * math.sin(i / 180.0 * math.pi)
  oled.pixel(int(64-x),int(32-y),1)
  
# show 秒針,每秒計算6度 , 一圈 360/6 = 60秒
for j in range (0,361,6) :
    x = 18 * math.cos(j/ 180.0 * math.pi)
    y = 18 * math.sin(j/ 180.0 * math.pi)
    oled.line(64,32,int(64-x),int(32-y),1) #畫秒針在畫布上
    oled.show() #顯示
    delay(1000) #等1 sec
    oled.line(64,32,int(64-x),int(32-y),0) # 清除秒針在畫布上
    oled.show()
