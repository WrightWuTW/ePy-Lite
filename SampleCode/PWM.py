from machine import PWM,Pin

pwm0 = PWM(Pin.board.PWM0,freq=50,duty=50) 
pwm0.duty(99)
pwm0.freq(1000)

pwm1 = PWM(Pin.board.PWM1,freq=200,duty=50) 
pwm1.duty(80)
pwm1.freq(1000)

pwm2 = PWM(Pin.board.PWM2,freq=100,duty=50) 
pwm2.duty(30)
pwm2.freq(2000)
   
pwm3 = PWM(Pin.board.PWM3,freq=150,duty=50) 
pwm3.duty(10)
pwm3.freq(500)
   
