from machine import Servo,delay

s1 = Servo(1)  # serve channel 1 is PWM0 , 2 is PWM1....4 is PWM3
s2 = Servo(2)
s3 = Servo(3)
s4 = Servo(4)
s_all = Servo(Servo.ALL_SERVO)
    
s1.calibration(1500,7000,1600,4100,3000) #(min,max,angle(0),angle(90),xxxx)
s2.calibration(1500,7000,1600,4100,3000)
s3.calibration(1500,7000,1600,4100,3000)
s4.calibration(1500,7000,1600,4100,3000)

s1.angle(90) # change to angle 90
delay(1000) #wait servo
s1.angle(180,1000) # change to angle 180 use 1000ms
delay(1000)
s1.angle(0,1000) # change to angle 0 use 1000ms
delay(1000)
s1.angle(180,1000) # change to angle 180 use 1000ms
delay(1000)
s1.angle(90)

for i in range (1,10):
    s_all.angle([180,180,180,180,2000]) # [s1 angle,s2 angle, s3 angle,s4 angle , active time]
    delay(2000)
    s_all.angle([0,0,0,0,5000])
    delay(2000)
    
