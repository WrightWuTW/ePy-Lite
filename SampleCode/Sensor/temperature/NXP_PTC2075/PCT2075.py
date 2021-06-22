# MicroPython TM1637 quad 7-segment LED display driver examples

# WeMos D1 Mini -- 4 Digit Display
# D1 (P2) ----- CLK
# D2 (P3) ----- DIO
# 3V3 ------------ VCC
# G -------------- GND

# PCT2075 --- 溫度 Sensor +-1度
# VCC --3.3V
# GND -- GND
# SDA -- SDA0
# SCL -- SCL0


from machine import I2C,Pin
import utime
import ustruct as struct
import tm1637


tm = tm1637.TM1637(clk=Pin.board.P19, dio=Pin.board.P18)

i2c =I2C(0,I2C.MASTER)

PCT2075_ADDR = 55
temp = bytearray(2)
counter = 0
try :
    utime.sleep_ms(1000)
    while True:
        if i2c.is_ready(PCT2075_ADDR) : # 檢查是否可以讀取
            counter = 0
           
            temp=i2c.recv(2,PCT2075_ADDR)
            T = struct.unpack('>h',temp) # 將讀到資料(2的補數 轉成 數字 , Little endding)
            temp_c = int (T[0])/32*125/1000 # 數據只有11 bit , 所以有 5bit 需要移除 ,2^5 =32 ,每一刻度代表 .125度
            temp_c = round(temp_c,2)  #取到小數第二位
            print ('{}.{}'.format(int(temp_c),int (temp_c*0.1*100)))
            tm.show('{}{}'.format(int(temp_c),int (temp_c*0.1*100)),True)  #顯示溫度到 TM1637上 , : 代替小數點
            utime.sleep_ms(100)
        else:
            counter = counter+1
            print (counter)
            utime.sleep_ms(100)
        if counter > 30 :
            
            tm.show('1Err')   #I2C 讀取錯誤
            break
except :
    tm.show(' Err')  #系統錯誤
    