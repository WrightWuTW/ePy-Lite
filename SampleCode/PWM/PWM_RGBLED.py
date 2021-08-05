'''
	PWM RGB LED
	GND --  GND
	PWM0 -- Green LED
	PWM1 -- Red LED
	PWM2 -- Blue LED

'''
from machine import PWM,Pin
import utime
pwmg= PWM(Pin.epy.PWM0,freq=1000,duty=0)
pwmr= PWM(Pin.epy.PWM1,freq=1000,duty=0)
pwmb= PWM(Pin.epy.PWM2,freq=1000,duty=0)
rainbow_color=[[pwmg,pwmr],[pwmb,pwmg],[pwmr,pwmb]]
def rainbow():
	for color in rainbow_color :
		for duty in range (0,100):
			color[0].duty(duty)
			utime.sleep_ms(10)
			
		for duty in range (100,-1,-1):
			color[1].duty(duty)
			utime.sleep_ms(10)
for duty in range (0,100):
	pwmr.duty(duty)
	utime.sleep_ms(10)
for i in range(100):
	rainbow()
	
'''
color_list=[ pwmr ,pwmg ,pwmb]
def Breathing_light():
	for color in color_list :
		for i in range (times):
			for r_duty in range (0,100):
				color.duty(r_duty)
				utime.sleep_ms(10)
			utime.sleep_ms(50)	
			for r_duty in range (100,-1,-1):
				color.duty(r_duty)
				utime.sleep_ms(10)
			utime.sleep_ms(50)		
'''