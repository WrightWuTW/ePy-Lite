from machine import RTC,LED,delay
ledy =LED('ledy')
rtc=RTC()
def tick_cb():
	ledy.toggle()

rtc.datetime ((2021,7,21,2,4,12,3,1))

rtc.tickcallback(tick_cb)

while True:
	delay (100)
	machine.stop()
