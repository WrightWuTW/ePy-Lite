from machine import LED,delay

ledR = LED('ledr')
ledY = LED('ledy')
ledG = LED('ledg')

ledR.off()
ledY.off()
ledG.off()
delay(1000)
ledR.on()
ledY.on()
ledG.on()

while True:
    ledG.toggle()
    delay(1000) 
