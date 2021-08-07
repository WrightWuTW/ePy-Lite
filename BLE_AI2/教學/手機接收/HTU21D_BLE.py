'''
  ePy Lite 內建BLE Module (UART1)
  傳輸 所讀取到的溫濕度 到手機上，搭配 Ai2 手機App (ePy_BLE_Read(HTU21D)_Write.aia)
  HTU21D --- ePy Lite
  VCC (+)  --> 3.3V
  GND (-)  --> GND
  SDA (DA) --> P17_SCL0
  SCL (CL) --> P16_SDA0
'''
from machine import I2C,UART

import utime
HTU21D_ADDR = 0x40
temp=bytearray(2)
i2c0=I2C(0,I2C.MASTER,baudrate=400000)
ble = UART(1,115200)
ble.write('AT+MODE_DATA\r\n')

while True:
    i2c0.send(0xE3,HTU21D_ADDR)
    utime.sleep_ms(50)
    i2c0.recv(temp,HTU21D_ADDR)
    rawTemperature = temp[0]<<8 | temp [1]
    Temperature = round((0.002681 * float(rawTemperature) - 46.85),2)
    #print (Temperature)
    ble.write('T = {}\r\n'.format (Temperature))
    utime.sleep(1)
    
    #read_Humidity():
    temp=bytearray(3)
    i2c0.send(0xE5,HTU21D_ADDR)
    utime.sleep_ms(50)
    i2c0.recv(temp,HTU21D_ADDR)
    rawHumidity = temp[0]<<8 | temp [1]
    rawHumidity ^= 0x02; #clear status bits, humidity always returns xxxxxx10 in the LSB field
    Humidity = round((0.001907 * float(rawHumidity) - 6),2)
    #print (Humidity)
    ble.write('H = {}\r\n'.format (Humidity))
    utime.sleep(1)
    
