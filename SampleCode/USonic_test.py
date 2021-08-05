from machine import USonic,Pin
import utime

su0=USonic(0, Pin.board.P15) # Echo pin is P17(fix) , Trig is P15
su1=USonic(1, Pin.board.P14) # Echo pin is P16(fix) , Trig is P14
su2=USonic(2, Pin.board.P13) # Echo pin is P9(fix) , Trig is P13
su3=USonic(3, Pin.board.P12) # Echo pin is P8(fix) , Trig is P12
su4=USonic(4, Pin.board.P11) # Echo pin is P7(fix) , Trig is P11
su5=USonic(5, Pin.board.P10) # Echo pin is P6(fix) , Trig is P10

while True:
	print ('USonic 0 dist is :',round(su0.distance()))
	print ('USonic 1 dist is :',round(su1.distance()))
	print ('USonic 2 dist is :',round(su2.distance()))
	print ('USonic 3 dist is :',round(su3.distance()))
	print ('USonic 4 dist is :',round(su4.distance()))
	print ('USonic 5 dist is :',round(su5.distance()))
	utime.sleep_ms(1000)
	print ('--------------------------------------------')
	