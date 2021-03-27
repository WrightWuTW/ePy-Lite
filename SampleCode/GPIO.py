from machine import LED,delay,Pin

p0 = Pin(Pin.board.P0,Pin.OUT) # P0 Output GPIO
p1 = Pin(Pin.board.P1,Pin.IN)  #P1 Input GPIO
while True:
    p0.value(1) # Output High
    print ('P0 output High')
    print ('P1 input is {}'.format(p1.value()))
    delay(500)
    p0.value(0) # Output Low
    print ('P0 output Low')
    print ('P1 input is {}'.format(p1.value()))
    delay(500)
