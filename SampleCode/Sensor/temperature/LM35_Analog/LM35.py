'''
溫度 LM35
Out -- AIN0 
GND -- GND
VCC -- 3.3V
'''
from machine import UART,ADC,Pin,LED
import utime
rled=LED('ledr')
gled=LED('ledg')
rgbled = LED(LED.RGB)

rled.off()
gled.off()

adc0=ADC(Pin.board.AIN0)

count = 0
while True:
    ''' Lite ADC have 12bit '''
    
    adc_0 = adc0.read() >> 2
    # temp = (adc_val /1024(10bit) *ADC_VCC ) *0.01 oC
    temp = (adc_0 /1024*3.3)/0.01
    print('{:3.2f} oC'.format(temp))
    utime.sleep_ms(1000)

