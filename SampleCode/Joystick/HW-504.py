
from machine import Pin,ADC,delay,Servo

Ax = ADC(Pin.epy.AIN2) 
Ay = ADC(Pin.epy.AIN1)
SW = ADC(Pin.epy.AIN0)

s1 = Servo(3)  #PWM2
s2 = Servo(4)  #PWM3

while True :
    print ('XVR = {} , YVR = {} , SW = {}'.format(Ax.read(),Ay.read(),SW.read()))
    s1.angle(int ((180/4096)*Ax.read()))
    s2.angle(int ((180/4096)*Ay.read()))
    delay(50)
    