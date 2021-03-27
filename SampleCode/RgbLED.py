
from machine import LED,delay

ledrgb = LED(LED.RGB)

while True:
    for i in range(1,61,3):
        for color in range(10,101,10):
            ledrgb.rgb_write(i,color,0,0)
            delay(20) 
            
    for i in range(2,61,3):
        for color in range(10,101,10):
            ledrgb.rgb_write(i,0,color,0)
            delay(20) 
        
    for i in range(3,61,3):
        for color in range(10,101,10):
            ledrgb.rgb_write(i,0,0,color)
            delay(20) 
