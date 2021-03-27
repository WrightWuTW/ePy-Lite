from machine import UART

uart= UART(3,115200,bits=8,parity=None, stop=1)
uart.write('AT\r\n')
ret = uart.readline()

uart.read(10) # read 10 characters, returns a bytes object

buf = bytearray(10)
uart.readinto(buf) # read and store into the given buffer


uart.write('abc') # write the 3 characters
uart.readchar() # read 1 character and returns it as an integer
uart.writechar(42) # write 1 character
uart.any() # returns the number of characters waiting
uart.deinit() # turn off the UART bus
