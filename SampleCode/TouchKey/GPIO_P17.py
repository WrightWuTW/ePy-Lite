'''
Touch Key
SIG --> P17
VCC --> 3.3V
GND --->GND 

when Touch the LED(Y) will off P17 is High)
release touch LED(Y) will on ( P17 is Low)
'''
from machine import Pin,LED
import utime
ledy = LED('ledy')
ledg = LED('ledg')
p17 = Pin(Pin.board.P17,Pin.IN)

ledg.off()
while True:
    
    print (p17.value())
    if p17.value() == 0 :
        ledy.on()
    else:
        ledy.off()
        
    utime.sleep_ms(500)
    
