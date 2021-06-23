# need update ePy-Lite micropython image to V1.5 

from machine import UART,LED,Switch,Timer
import utime,gc

BLE_uart = UART(1,115200) #open BLE UART Port

#define two RGB LED show templet
templet0 =  [['01','01','00','00','00'],\
            ['01','02','00','00','00'],\
            ['01','03','00','00','00'],\
            ['01','04','00','00','00'],\
            ['01','05','00','00','00'],\
            ['01','01','1F','00','00'],\
            ['01','02','1F','00','00'],\
            ['01','03','1F','00','00'],\
            ['01','04','1F','00','00'],\
            ['01','05','1F','00','00'],\
            ['01','01','00','1F','00'],\
            ['01','02','00','1F','00'],\
            ['01','03','00','1F','00'],\
            ['01','04','00','1F','00'],\
            ['01','05','00','1F','00'],\
            ['01','01','00','00','1F'],\
            ['01','02','00','00','1F'],\
            ['01','03','00','00','1F'],\
            ['01','04','00','00','1F'],\
            ['01','05','00','00','1F']]
            
templet1 =  [['01','01','1F','00','00'],\
            ['01','01','00','00','00'],\
            ['01','02','1F','00','00'],\
            ['01','02','00','00','00'],\
            ['01','03','1F','00','00'],\
            ['01','03','00','00','00'],\
            ['01','04','1F','00','00'],\
            ['01','04','00','00','00'],\
            ['01','05','1F','00','00'],\
            ['01','05','00','00','00'],\
            ['01','06','1F','00','00'],\
            ['01','06','00','00','00'],\
            ['01','07','1F','00','00'],\
            ['01','07','00','00','00'],\
            ['01','08','1F','00','00'],\
            ['01','08','00','00','00'],\
            ['01','09','1F','00','00'],\
            ['01','09','00','00','00'],\
            ['01','0A','1F','00','00'],\
            ['01','0A','00','00','00']]            
            
# 定義廣播封包前識別碼 '7319', type '16' '08' 是廣播封包長度 8byte 
# len = 16 ,73, 19 ,ID, ,lednumber , Rcolor, Gcolor , Bcolor ; 最大可達30 byte
ADV_NAME ='08167319'
ID = '01'
ledNumber ='01'
Rcolor = '8F'
Gcolor = '00'
Bcolor = '00'

intev_time = 1000
counter = 0

ledy = LED('ledy')
ledr = LED('ledr')
ledg = LED('ledg')
ledrgb = LED(LED.RGB)

ledy.off()
ledr.off() 
ledg.off()

# 使用 KeyA 去做 templet 切換
keya = Switch('keya')

# 設定 0.5s 觸發時鐘 定時更改廣播訊息
tim_3 = Timer(3,freq = 2)

def SendAdvData (name,id,lednum,r,g,b):
    BLE_uart.write('AT+AD_SET=0,{0}{1}{2}{3}{4}{5}\r\n'.format(name,id,lednum,r,g,b))
    ledy.toggle()


# Timer callback function 定時改變廣播資訊
def timer_send(timer):
    global templet,counter
    
    SendAdvData (ADV_NAME,templet[counter][0],\
                            templet[counter][1],\
                            templet[counter][2],\
                            templet[counter][3],\
                            templet[counter][4])
    counter = counter+1 
    if counter >=20 :
        counter =0

# change BLE to Command Mode 
BLE_uart.write ('!CCMD@')
utime.sleep_ms(200)
BLE_uart.write ('!CCMD@')
utime.sleep_ms(200)

# disable BLE ADVERT then setting ADVERT function
BLE_uart.write('AT+ADVERT=0\r\n')
utime.sleep_ms(20)
BLE_uart.write('AT+ADV_INTERVAL=50\r\n')
utime.sleep_ms(20)
BLE_uart.write ('AT+ADVERT=1\r\n')
utime.sleep_ms(20)

tim_3.callback(timer_send)
templet = templet1
while True:
    free_mem = gc.mem_free()
    
    #check free memory ,use gc.collect() to release RAM 
    print (free_mem)
    if free_mem < 40000 :
        # collect memory need disable other interrupt 
       tim_3.callback(None)
       gc.collect()
       tim_3.callback(timer_send)
       
    if keya.value() :
        counter = 0
        if templet == templet0:
            templet = templet1
        else :
            templet = templet0
    utime.sleep_ms(500)
    
BLE_uart.write('AT+ADV_DATA_SCAN=0\r\n')
utime.sleep_ms(20)
BLE_uart.write('AT+ROLE=P\r\n') 
utime.sleep_ms(1000)

