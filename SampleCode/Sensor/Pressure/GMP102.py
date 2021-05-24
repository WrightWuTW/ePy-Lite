from machine import I2C,delay,LED
import math
import ustruct as struct

GMP102_ADDR = 0x6C #SA0 connect to GND
GMP102_Soft_RST    = b'\x00\x24'
GMP102_STATUS      = 0x02
GMP102_PRESSURE    =  0x06
GMP102_TEMPERATURE =  0x09
GMP102_COMMAND_PRESS = b'\x30\x09' #single shot 
GMP102_COMMAND_TEMP  = b'\x30\x08' #single shot 
GMP102_SET_RAW_TEMP  = b'\xA5\x00'
GMP102_SET_RAW_PRESS  = b'\xA5\x02'
GMP102_SET_OSR = 0xA6
GMP102_CALIB00     =  0xAA
#Total calibration register count: AAh~BBh total 18
GMP102_CALIBRATION_REGISTER_COUNT =18
GMP102_CALIB_SCALE_FACTOR = [1.0,1.0e-5,1.0e-10,1.0e-05,1.0e-10,1.0e-15,1.0e-12,1.0e-17,1.0e-21]

#press_data = bytearray(4) 
temp_data = bytearray(2)

p = [0]*9
led = LED('ledg')
led.off()
def GP102_DATA_Ready(i2c_bus):
    i2c_bus.send(GMP102_STATUS,GMP102_ADDR)
    if (i2c_bus.recv(1,GMP102_ADDR)[0]&0x01) == 0x01:
        return True
    else :
        return False

def GMP102_init(i2c_bus):
    i2c_bus.send(GMP102_Soft_RST,GMP102_ADDR)
    
    delay(100)
    i2c_bus.send(GMP102_SET_OSR,GMP102_ADDR)
    i2c_bus.send(0x07,GMP102_ADDR)
    
    i2c_bus.send(GMP102_CALIB00,GMP102_ADDR)
    calib_data = i2c_bus.recv(GMP102_CALIBRATION_REGISTER_COUNT,GMP102_ADDR)
    i2c_bus.send(GMP102_CALIB00,GMP102_ADDR)
    i2c_bus.send(b'\x00\x00\x00\x00',GMP102_ADDR)
    return calib_data

def GMP102_PRESSURE_READ(i2c_bus):
    press_data = bytearray(4) 
    i2c_bus.send(GMP102_SET_RAW_PRESS,GMP102_ADDR)
    i2c_bus.send(GMP102_COMMAND_PRESS,GMP102_ADDR)
    
    while GP102_DATA_Ready (i2c_bus) != True :
       pass
    i2c_bus.send ( GMP102_PRESSURE,GMP102_ADDR)
    press_data = i2c_bus.recv(3, GMP102_ADDR)
    data = list(press_data)
    data.insert (0,0)
    return(struct.unpack('>i',bytearray(data))[0])

def GMP102_TEMP_READ(i2c_bus):
    data = bytearray(2)
    temp = 0
    i2c_bus.send(GMP102_SET_RAW_TEMP,GMP102_ADDR)
    i2c_bus.send(GMP102_COMMAND_TEMP,GMP102_ADDR)
    
    while GP102_DATA_Ready (i2c_bus) != True :
       pass
    i2c_bus.send ( GMP102_TEMPERATURE,GMP102_ADDR)
    data = i2c_bus.recv(2, GMP102_ADDR)
    temp = struct.unpack('>h',data)
    return(temp[0])
    
GMP102_i2c= I2C(0,I2C.MASTER,baudrate=100000)
CAB = GMP102_init(GMP102_i2c)
for i in range(0,9):
    p[i] = ((struct.unpack('>h',CAB[i*2:i*2+2]))[0]/4) * math.pow(10,CAB[(i*2)+1] & 3 )* GMP102_CALIB_SCALE_FACTOR[i]

while True:
    press_raw=GMP102_PRESSURE_READ(GMP102_i2c)
    temp_raw=GMP102_TEMP_READ(GMP102_i2c)

    fP_Pa =p[0] +p[1]*temp_raw + p[2]*temp_raw**2 + \
            p[3]*press_raw + p[4]*temp_raw*press_raw + \
            p[5]*(temp_raw**2)*press_raw + \
            p[6]*math.pow(press_raw,2) + \
            p[7]*temp_raw*math.pow(press_raw,2) + \
            p[8]*math.pow(temp_raw,2)*math.pow(press_raw,2)
    altm = float(44307.694 *(1-(math.pow((fP_Pa/101325),0.190284))))

    print ('氣壓={:.2f}pa  , 高度={:3.2f} m'.format(fP_Pa,altm))
    delay(1000)

