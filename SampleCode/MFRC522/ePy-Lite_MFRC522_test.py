"""
 ePy-Lite_MFRC522.py
------------------------------------------ 
  ePy-Lite   MFRC522 Reader
  Pin        Signal     Pin
  ---------------------------------------- 
  P9(CS)     SS         SDA(SS)
  P8(CLK)    Clock      SCK  
  P6(MOSI)   Data in    MOSI 
  P7(MISO)   Data Out   MISO
                        IRQ
  GND        GND        GND
  P10        RST/Reset  RST
  3V3        3V3        3V3
"""

from micropython import const
from machine import SPI, Pin
from machine import Switch   #Get button KEY library
import utime
import mfrc522

spi_0 = None
test  = None
# test  = 1 #write test

def do_read(addr):
  (stat, tag_type) = rdr.request(rdr.REQIDL)  #Search for RFID cards
  
  if stat == rdr.OK:  #Find the card
    (stat, raw_uid) = rdr.anticoll()  #Read RFID card number

    if stat == rdr.OK:
      print("New card detected")
      print("  - tag type: 0x%02X" % tag_type)
      print("  - uid   : 0x%02X%02X%02X%02X" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
      print("")
  
      if rdr.select_tag(raw_uid) == rdr.OK:
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
  
        if rdr.auth(rdr.AUTHENT1A, addr, key, raw_uid) == rdr.OK:
          print("Address %d data: %s" % (addr,rdr.read(addr)))
          rdr.stop_crypto1()
        else:
          print("Authentication error")
      else:
        print("Failed to select tag")

def do_write(addr, data):
  (stat, tag_type) = rdr.request(rdr.REQIDL)  #Search for RFID cards

  if stat == rdr.OK:  #Find the card
    (stat, raw_uid) = rdr.anticoll()  #Read RFID card number

    if stat == rdr.OK:
      print("New card detected")
      print("  - tag type: 0x%02x" % tag_type)
      print("  - uid   : 0x%02X%02X%02X%02X" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
      print("")

      if rdr.select_tag(raw_uid) == rdr.OK:
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

        if rdr.auth(rdr.AUTHENT1A, addr, key, raw_uid) == rdr.OK:
          stat = rdr.write(addr, data)
          rdr.stop_crypto1()
          if stat == rdr.OK:
            print("Data written to card")
          else:
            print("Failed to write data to card")
        else:
          print("Authentication error")
      else:
        print("Failed to select tag")

# Start Function
if __name__=="__main__":
  buf = bytearray(16)
  Num1 = 0
  KeyA = Switch('keya')    #Create button A
  rdr = mfrc522.MFRC522(Pin.board.P10, Pin.board.P9)  #rst, cs

  utime.sleep_ms(1000)
  print("")
  if test != None:
    print("Place card before reader to write address 0x08")
  else:
    print("Place card before reader to read from address 0x08")
  print("")

  while True:
    if test != None:
      for i in range(16):
        buf[i] = Num1 + i
      do_write(8,buf)
      Num1=Num1+1
    else:
      do_read(8)

    if (KeyA.value()) == True:      #Press A Key
      break
    utime.sleep_ms(500)

  # spi_0.deinit()