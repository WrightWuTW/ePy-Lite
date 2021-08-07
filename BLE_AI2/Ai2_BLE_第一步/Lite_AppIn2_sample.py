from machine import UART,delay,LED
# Lite BLE on UART port 1, baudrate is 115200)
ble=UART(1,115200,timeout=200)
ledy = LED('ledy')
ledr = LED('ledr')

#確保 BLE 回到  CMD mode
ble.write('!CCMD@')
delay(150)
ble.write('!CCMD@')
delay(150)
# enable BLE System MSG
ble.write('AT+EN_SYSMSG=1\r\n')
delay(50)

while True:
    msg = ble.readline()
    print (msg)
    recv_data = str(msg,'utf-8') # 200ms will return a data
    print (recv_data)
    if recv_data == 'A' :
        ledy.toggle()
    if recv_data == 'B' :
        ledr.toggle()
    if recv_data == 'b' :
        ledr.toggle()  
        
    
    
    



          