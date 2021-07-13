import tm1637,math
from machine import Pin,delay
from machine import USonic
sonic=USonic(0)
tm = tm1637.TM1637(clk=Pin.board.P0, dio=Pin.board.P1)
while True:
  dis = math.floor(sonic.distance()) #取整數
  tm.number(dis)
delay(200)
