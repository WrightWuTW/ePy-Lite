from machine import RTC

today = (2021,2,22,1,0,25,18,0) # (year,month,day,weekly,hour,min,sec,sub) 

rtc = RTC()

rtc.datetime(today)
   
while True:
    print (rtc.datetime())
    machine.delay(1000)
