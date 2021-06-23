# need update ePy-Lite micropython image to V1.5 

from machine import LED,Pin,ADC,Switch,UART
import utime,micropython,sys,gc


# setting 接收 ADVERT information 

ADV_NAME ='08167319'
myID = '01'

ledy = LED('ledy')
ledr = LED('ledr')
ledg = LED('ledg')
ledrgb = LED(LED.RGB)


ledy.off() 
ledr.off()
ledg.off()

keya = Switch('keya')

#使用  UART1 連接 BLE，並增加接收 Buffer 
BLE_uart = UART(1,115200,read_buf_len=1024)
       
# 確認切到 command mode
BLE_uart.write ('!CCMD@')
utime.sleep_ms(200)
BLE_uart.write ('!CCMD@')
utime.sleep_ms(200)
ledy.toggle()

# 改變 BLE mode to PERIPHERAL mode (client )
BLE_uart.write ('AT+ROLE=?\r\n') 
utime.sleep_ms(20)
Resp = BLE_uart.readline()
 
if 'PERIPHERAL' in Resp:
    BLE_uart.write ('AT+ROLE=C\r\n') 
    utime.sleep_ms(500)
    while True:
        input_data = BLE_uart.readline() 
        if 'READY OK' in input_data:
            break
ledy.toggle()    

# disable ADVERT and change SCAN function
BLE_uart.write('AT+ADV_DATA_SCAN=0\r\n')
utime.sleep_ms(20)
msg = BLE_uart.readline()

BLE_uart.write('AT+SCAN_INTERVAL=200\r\n')
utime.sleep_ms(20)
msg = BLE_uart.readline()

BLE_uart.write('AT+SCAN_WINDOW=100\r\n')
utime.sleep_ms(20)
msg = BLE_uart.readline()
BLE_uart.write('AT+ADV_DATA_SCAN=1\r\n')
utime.sleep_ms(20)
msg = BLE_uart.readline()


# change RGB LED lightness to 100%
ledrgb.lightness(100)

while True:
    #collect the Free MemoryError
    gc.collect()
    
    # read SCAN ADVERT data , 並轉換為字串
    data = str(BLE_uart.readline(),'utf-8')
    # 使用空白 切割 字串
    ss = data.split(' ')
     
    #只運作 具有四段以上，並且第四段必須大於 18個 bytearray  
    if len(ss) > 3 and len(ss[3]) >=18:
        name = ss[3][0:8]
        id = ss[3][8:10]
        
        # 濾出 廣播名字與 ID相同的 廣播資訊
        if ADV_NAME == name and id == myID:
            
            ledNumber = int (ss[3][10:12],16)
            RColor = int (ss[3][12:14],16)
            GColor = int (ss[3][14:16],16)
            BColor = int (ss[3][16:18],16)

            ledg.toggle()
            #依據資訊顯示 RGB LED
            ledrgb.rgb_write(ledNumber,RColor,GColor,BColor)
        ledy.toggle()
 
BLE_uart.write ('AT+ADV_DATA_SCAN=0\r\n')
utime.sleep_ms(20)
BLE_uart.write ('AT+ROLE=P\r\n') 
utime.sleep_ms(1000)
