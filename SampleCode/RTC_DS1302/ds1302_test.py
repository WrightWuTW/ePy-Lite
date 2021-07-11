from machine import Pin
from ds1302 import DS1302

rtc = DS1302(Pin.board.P17,Pin.board.P16,Pin.board.P15)
print (rtc.DateTime())
rtc.DateTime([2021,7,11,7,30,14,3,15])
print ('Now is :',rtc.DateTime())

rtc.Hour(10)
print ('Now Hour is :',rtc.Hour())

'''
rtc.Second() 
Month()
Year()
Minute()
Second()
Day()
Weekday()
'''
