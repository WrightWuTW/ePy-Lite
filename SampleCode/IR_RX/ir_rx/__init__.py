# ir_rx __init__.py Decoder for IR remote control using synchronous code
# IR_RX abstract base class for IR receivers.

# Author: Peter Hinch
# Copyright Peter Hinch 2020-2021 Released under the MIT license

from machine import Timer, Pin
from array import array
from utime import ticks_us

# Save RAM
# from micropython import alloc_emergency_exception_buf
# alloc_emergency_exception_buf(100)


# On 1st edge start a block timer. While the timer is running, record the time
# of each edge. When the timer times out decode the data. Duration must exceed
# the worst case block transmission time, but be less than the interval between
# a block start and a repeat code start (~108ms depending on protocol)

class IR_RX():
    # Result/error codes
    # Repeat button code
    REPEAT = -1
    # Error codes
    BADSTART = -2
    BADBLOCK = -3
    BADREP = -4
    OVERRUN = -5
    BADDATA = -6
    BADADDR = -7

    def __init__(self, pin, nedges, tblock, callback, *args):  # Optional args for callback
        self._pin = pin
        self._nedges = nedges
        self._tblock = tblock
        self.callback = callback
        self.args = args
        self._errf = lambda _ : None
        self.verbose = False

        self._times = array('i',  (0 for _ in range(nedges + 1)))  # +1 for overrun
        self.tim0 = Timer(0, freq = 1000000)
        self.tim0chan = self.tim0.channel(Timer.IC, pin = self._pin, polarity = Timer.RISING)
        self.tim0chan.callback(self._cb_pin)
        self.edge = 0
        self.tim = Timer(1)  # Hardware Timer 1
        self.cb = self.decode

    # Pin interrupt. Save time of each edge for later decode.
    def _cb_pin(self, line):
        t = self.tim0chan.capture()
        # On overrun ignore pulses until software timer times out
        if self.edge <= self._nedges:  # Allow 1 extra pulse to record overrun
            if not self.edge:  # First edge received
                self.tim.init(freq= int(1/self._tblock *1000) , mode=Timer.ONESHOT, callback=self.cb)
            self._times[self.edge] = t
           
            self.edge += 1

    def do_callback(self, cmd, addr, ext, thresh=0):
        self.edge = 0
        if cmd >= thresh:
            self.callback(cmd, addr, ext, *self.args)
        else:
            self._errf(cmd)

    def error_function(self, func):
        self._errf = func

    def close(self):
        self.tim0chan.callback(None)
        self.tim.deinit()
