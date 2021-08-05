# nec.py Decoder for IR remote control using synchronous code
# Supports NEC protocol.
# For a remote using NEC see https://www.adafruit.com/products/389

# Author: Peter Hinch
# Copyright Peter Hinch 2020 Released under the MIT license

from utime import ticks_us, ticks_diff
from ir_rx import IR_RX

class NEC_ABC(IR_RX):
    def __init__(self, pin, extended, callback, *args):
        # Block lasts <= 80ms (extended mode) and has 68 edges
        super().__init__(pin, 34, 80, callback, *args)
        self._extended = extended
        self._addr = 0

    def decode(self, _):
        try:
            if self.edge > 34:
                raise RuntimeError(self.OVERRUN)
            width = ticks_diff(self._times[1], self._times[0])
            
            if width < 1700:  # 9ms leading mark for all valid data
                raise RuntimeError(self.BADSTART)
            #width = ticks_diff(self._times[2], self._times[1])
            if width > 3000:  # 4.5ms space for normal data
             
                if self.edge < 34:  # Haven't received the correct number of edges
                    raise RuntimeError(self.BADBLOCK)
                # Time spaces only (marks are always 562.5µs)
                # Space is 1.6875ms (1) or 562.5µs (0)
                # Skip last bit which is always 1
                addr = 0
                cmd = 0
                for edge in range(1, 17, 1): 
                    addr >>= 1
                    if ticks_diff(self._times[edge + 1], self._times[edge]) > 1220:
                        addr |= 0x8000
                for edge in range(17, 33, 1): 
                     cmd >>= 1
                     if ticks_diff(self._times[edge + 1], self._times[edge]) > 1220:
                        cmd |= 0x8000

            elif width > 1700: # 2.5ms space for a repeat code. Should have exactly 4 edges.
                raise RuntimeError(self.REPEAT if self.edge == 1 else self.BADREP)  # Treat REPEAT as error.
            else:
                raise RuntimeError(self.BADSTART)
            addr8 = addr & 0xff  # 8 bit addr
            cmd8 = cmd & 0xff

            if cmd8 != (cmd >> 8) ^ 0xff:
                raise RuntimeError(self.BADDATA)
            if addr8 != ((addr >> 8) ^ 0xff) & 0xff:  # 8 bit addr doesn't match check
                if not self._extended:
                    raise RuntimeError(self.BADADDR)
                addr |= addr & 0xff00  # pass assumed 16 bit address to callback
            self._addr = addr
        except RuntimeError as e:
            cmd = e.args[0]
            addr = self._addr if cmd == self.REPEAT else 0  # REPEAT uses last address
        # Set up for new data burst and run user callback
        self.do_callback(cmd, addr, 0, self.REPEAT)

class NEC_8(NEC_ABC):
    def __init__(self, pin, callback, *args):
        super().__init__(pin, False, callback, *args)

class NEC_16(NEC_ABC):
    def __init__(self, pin, callback, *args):
        super().__init__(pin, True, callback, *args)
