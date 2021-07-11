'''
Vin --- +
GND --- -
P13 --- IN1
P12 --- IN2
P11 --- IN3
P10 --- IN4
'''
from StepMotor import StepperMotor as Stepper
from machine import Pin
import utime
in1 = Pin(Pin.epy.P13,Pin.OUT)
in2 = Pin(Pin.epy.P12,Pin.OUT)
in3 = Pin(Pin.epy.P11,Pin.OUT)
in4 = Pin(Pin.epy.P10,Pin.OUT)

stepp = Stepper(in1,in3,in2,in4,microsteps=None)

def motor_angle(dir,angle, s):
    if s == 3:
        step = (4096//360*angle)
    if s == 2:
        step = (2048//360*angle)
    if s == 1:
        step = (2048//360*angle) 
        
    for i in range (step):
        stepp.onestep(direction=dir,style=s )
        utime.sleep_ms(3)

# --半步 驅動--##
motor_angle(2,180,3) #逆時鐘 ,180度 , 半步 =3
utime.sleep_ms(1000)
motor_angle(1,180,3) #順時鐘
utime.sleep_ms(1000)
# --全步 驅動--##
motor_angle(2,180,2) #逆時鐘 ,180度 , 全步 =2
utime.sleep_ms(1000)
motor_angle(1,180,2)
utime.sleep_ms(1000)
# --單步 驅動--##
motor_angle(2,180,1)  #逆時鐘 ,180度 ,單步 =1
utime.sleep_ms(1000)
motor_angle(1,180,1)
utime.sleep_ms(1000)
stepp.release() 
