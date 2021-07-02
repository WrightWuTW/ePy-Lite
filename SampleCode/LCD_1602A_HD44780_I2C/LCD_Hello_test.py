"""Implements a HD44780 character LCD connected via PCF8574 on I2C."""
'''
ePy Lite - > LCD 1602A
VIN(5V)  --> VCC
P17(SCL0)--> SCL
P16(SDA0)--> SDA
GND   -----> GND

'''
from lcdapi import LcdApi

from machine import I2C, delay, millis
from i2c_lcd import I2cLcd

# The PCF8574 has a jumper selectable address: 0x20 - 0x27
DEFAULT_I2C_ADDR = 0x27

def test_main():
    """Test function for verifying basic functionality."""
    print("Running test_main")
    
    ''' use I2C0 , and must change baudrate to 50kHz '''
    i2c = I2C(0, I2C.MASTER,baudrate=50000)
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)
    lcd.putstr("It Works!\nSecond Line")
    delay(3000)
    lcd.clear()
    count = 0
    while True:
        lcd.move_to(0, 0)
        lcd.putstr("%7d" % (millis() // 1000))
        delay(1000)
        count += 1
        if count % 10 == 3:
            print("Turning backlight off")
            lcd.backlight_off()
        if count % 10 == 4:
            print("Turning backlight on")
            lcd.backlight_on()
        if count % 10 == 5:
            print("Turning display off")
            lcd.display_off()
        if count % 10 == 6:
            print("Turning display on")
            lcd.display_on()
        if count % 10 == 7:
            print("Turning display & backlight off")
            lcd.backlight_off()
            lcd.display_off()
        if count % 10 == 8:
            print("Turning display & backlight on")
            lcd.backlight_on()
            lcd.display_on()

#if __name__ == "__main__":
test_main()
