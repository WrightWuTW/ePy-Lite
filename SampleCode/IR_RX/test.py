# test.py Test program for IR remote control decoder
# Supports Pyboard, ESP32 and ESP8266

# Author: Peter Hinch
# Copyright Peter Hinch 2020 Released under the MIT license

# Run this to characterise a remote.

import utime
import gc
from machine import Pin
import tm1637
from ir_rx.print_error import print_error  # Optional print of error codes
# Import all implemented classes
#
from ir_rx.sony import SONY_12, SONY_15, SONY_20
from ir_rx.philips import RC5_IR, RC6_M0
from ir_rx.mce import MCE
from ir_rx.nec import NEC_8, NEC_16

IrKeyDict= {'0xba45':'1','0xb946':'2','0xb847':'3','0xbb44':'4',\
            '0xbf40':'5','0xbc43':'6','0xf807':'7','0xea15':'8',\
            '0xf609':'9','0xe619':'0','0xe916':'*','0xf20d':'#',\
            '0xe718':'up','0xad52':'down','0xa55a':'right','0xf708':'left',\
            '0xe31c':'OK'}

p = Pin(Pin.epy.P15, Pin.IN)
tm = tm1637.TM1637(clk=Pin.epy.P18, dio=Pin.epy.P19)
tm.show('8888') 

# User callback
def cb(data, addr, ctrl):
    if data < 0:  # NEC protocol sends repeat codes.
        print('Repeat code.')
    else:
        print('Data {:02x} Addr {:04x} Ctrl {:02x}'.format(data, addr, ctrl))
        tm.show ('    ')
        tm.show(IrKeyDict.get(str(hex(data))))

def test(proto=1):
    classes = (NEC_8, NEC_16, SONY_12, SONY_15, SONY_20, RC5_IR, RC6_M0, MCE)
    ir = classes[proto](p, cb)  # Instantiate receiver
    #ir.error_function(print_error)  # Show debug information
    #ir.verbose = True
    # A real application would do something here...
    try:
        while True:
            print('running')
            utime.sleep(5)
            gc.collect()
    except KeyboardInterrupt:
        ir.close()

# **** DISPLAY GREETING ****
s = '''Test for IR receiver. Run:
from ir_rx.test import test
test() for NEC 8 bit protocol,
test(1) for NEC 16 bit,
test(2) for Sony SIRC 12 bit,
test(3) for Sony SIRC 15 bit,
test(4) for Sony SIRC 20 bit,
test(5) for Philips RC-5 protocol,
test(6) for RC6 mode 0.
test(7) for Microsoft Vista MCE.

Hit ctrl-c to stop, then ctrl-d to soft reset.'''
test(1)
print(s)
