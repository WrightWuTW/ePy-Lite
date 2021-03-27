
from machine import LED
from machine import Timer

ledG = LED('ledg')
ledR = LED('ledr')
ledY = LED('ledy')


def tick(timer):
    ledG.toggle()
    
def tick1(timer):
    ledR.toggle()
    
def tick2(timer):
    ledY.toggle()
     
tim = Timer(3,freq = 1)
tim.callback (tick)
tim1 = Timer(2,freq = 2)
tim1.callback(tick1)
tim2 = Timer(1,freq = 3)
tim2.callback(tick2)
 
while True:
    pass
    
   
