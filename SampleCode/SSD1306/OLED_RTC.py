import ssd1306
from machine import I2C,delay,RTC
i2c = I2C(0,I2C.MASTER,baudrate=400000)
disp = ssd1306.SSD1306_I2C(128,64,i2c)

today = (2021,3,16,3,9,0,0,0)

rtc = RTC()
rtc.datetime(today)

while True:
    disp.fill(0)
    time=rtc.datetime()
    disp.text('Date:{yy}/{mm}/{dd}'.format(yy=time[0],mm=time[1],dd=time[2]),0,16,1)
    disp.text('time:{hh}:{mm}:{ss}'.format(hh=time[4],mm=time[5],ss=time[6]),0,36,1)
    disp.show()
    delay(900)

#clr screen
disp.fill(0)
disp.show()

disp.pixel(0,0,1)
disp.text('SSD1306',0,8,1)
disp.invert(1)
disp.invert(0)
