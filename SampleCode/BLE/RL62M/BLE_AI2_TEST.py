# main.py -- put your code here!
from machine import LED,Pin,ADC,Switch
import utime
import uos as os
import micropython,sys

ledy = LED('ledy')
ledr = LED('ledr')
ledg = LED('ledg')

ledy.off()
ledr.off()
ledg.off()

micropython.kbd_intr(-1)
while True:
    ch = sys.stdin.read(1)
    if ch == '/r':
        break
    
count =0
while True:
    ch = sys.stdin.read(2)
    if ch == 'Q0':
        break
    if ch == 'R0':
        ledr.toggle()
    if ch == 'G0':
        ledg.toggle()
    if ch == 'Y0':
        ledy.toggle()
    if ch == 'r0':
        ledr.on()
    if ch == 'g0':
        ledg.on()
    if ch == 'y0':
        ledy.on()
    if ch == 'r1':
        ledr.off()
    if ch == 'g1':
        ledg.off()
    if ch == 'y1':
        ledy.off()      
    print ('key=',ch)
    utime.sleep_ms(100)
        
micropython.kbd_intr(3)
