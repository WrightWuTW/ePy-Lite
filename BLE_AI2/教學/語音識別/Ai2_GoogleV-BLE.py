'''
BLE send 'A' CMD to open Lite's Y LED
send 'B' to Close Y LED
'''
from machine import I2C,UART,LED
import utime
HTU21D_ADDR = 0x40
temp=bytearray(2)
led = LED('ledy')
i2c0=I2C(0,I2C.MASTER,baudrate=400000)
ble = UART(1,115200)
ble.write('AT+MODE_DATA\r\n')

def Read_BLE ():
    msg = ble.read(ble.any())
    if msg != '' :
        return (msg)
    else :
        return (None)       
while True:
    m = str(Read_BLE(),'utf-8')
    print(m)
    if m == 'A' :
        led.off()
    elif m == 'B':
        led.on()
   
    i2c0.send(0xE3,HTU21D_ADDR)
    utime.sleep_ms(50)
    i2c0.recv(temp,HTU21D_ADDR)
    rawTemperature = temp[0]<<8 | temp [1]
    Temperature = round((0.002681 * float(rawTemperature) - 46.85),2)
    #print(Temperature)
    ble.write('T = {}\r\n'.format (Temperature))
    utime.sleep_ms(200)
    
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
    utime.sleep_ms(200)
    
