
from machine import ADC,Pin

adc0 = ADC(Pin.board.AIN0)
adc1 = ADC(Pin.board.AIN1)
adc2 = ADC(Pin.board.AIN2)
adc3 = ADC(Pin.board.AIN3)
adc4 = ADC(Pin.board.AIN4)
adc5 = ADC(Pin.board.AIN5)


while True:
    print ('ADC0=',adc0.read())
    machine.delay(1)
    print ('ADC1=',adc1.read())
    machine.delay(1)
    print ('ADC2=',adc2.read())
    machine.delay(1)
    print ('ADC3=',adc3.read())
    machine.delay(1)
    print ('ADC4=',adc4.read())
    machine.delay(1)
    print ('ADC5=',adc5.read())
    machine.delay(100)

