
from machine import LED
from machine import Switch

ledG = LED('ledg')
ledR = LED('ledr')
ledY = LED('ledy')

keyA = Switch('keya')
   
def KeyA_Function():
    print ('KeyA be pressed')
    ledG.toggle()
   
keyA.callback(KeyA_Function)

while True:
    pyb.delay(3000)
    pass
     
