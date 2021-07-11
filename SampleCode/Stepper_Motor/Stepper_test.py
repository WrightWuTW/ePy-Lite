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

def motor_ang(x):
    step = (4096//360*x)
    for i in range (step):
        stepp.onestep()
        utime.sleep_ms(1)

motor_ang(180)
utime.sleep_ms(1000)
motor_ang(180)
