'''
CMC GMFS02EVB
pin1 -- AIN0 (up)
pin4 -- AIN1 (down)
pin3 -- GND
pin2 -- 3.3V
'''
from machine import UART,ADC,Pin,LED
import utime
rled=LED('ledr')
gled=LED('ledg')
rgbled = LED(LED.RGB)

rled.off()
gled.off()
adc0=ADC(Pin.board.AIN0)
adc1=ADC(Pin.board.AIN1)
count = 0
while True:
    adc_0 = adc0.read()
    adc_1 = adc1.read()
    report0 = adc_0*3.3/(2**12)
    report1 = adc_1*3.3/(2**12)
    if (report0-report1 >= 1.2):
        if count==3:
            count=1
        else:
            count = count+1
        if count == 1:
            rgbled.rgb_write(1,255,0,0)
            rgbled.rgb_write(2,0,255,0)
            rgbled.rgb_write(3,0,0,255)  
        elif count ==2:
            rgbled.rgb_write(2,255,0,0)
            rgbled.rgb_write(3,0,255,0)
            rgbled.rgb_write(1,0,0,255) 
        elif count ==3:
            rgbled.rgb_write(3,255,0,0)
            rgbled.rgb_write(1,0,255,0)
            rgbled.rgb_write(2,0,0,255) 
        
    else :
        count = 0
        rgbled.off()
        
    print('{:3.2f}'.format(report0-report1))
    utime.sleep_ms(200)
