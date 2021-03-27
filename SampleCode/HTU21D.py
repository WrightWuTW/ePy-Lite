from machine import I2C
import utime

HTU21D_ADDR = 0x40  # I2C OLED 位址

temp=bytearray(3)
i2c0=I2C(0,I2C.MASTER)
i2c0.send(0xE3,0x40)
utime.sleep_ms(50)
i2c0.recv(temp,0x40)
rawTemperature = temp[0]<<8 | temp [1]
i2c0.deinit()
print (0.002681 * float(rawTemperature) - 46.85)
    
#read_Humidity():
temp=bytearray(3)
i2c0=I2C(0,I2C.MASTER)
i2c0.send(0xE5,0x40)
utime.sleep_ms(50)
i2c0.recv(temp,0x40)
i2c0.deinit()
rawHumidity = temp[0]<<8 | temp [1]
rawHumidity ^= 0x02; #clear status bits, humidity always returns xxxxxx10 in the LSB field
print (0.001907 * float(rawHumidity) - 6)
