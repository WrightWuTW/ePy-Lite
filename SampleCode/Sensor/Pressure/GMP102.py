"""
   ePy-Lite   GMP102
  -----------------
   GND        Pin1  GND
              Pin2  CSB
   P18_SDA0   Pin3  SDI/SDA
   P17_SCL0   Pin4  SCK/SCL
   GND        Pin5  SDO/SA0
   3V3        Pin6  VID
   GND        Pin7  GND
   3V3        Pin8  VCC

  GMP102 Application note for Calibrated Pressure Calculation
  https://github.com/GlobalMEMS/Application-Notes
  GlobalMEMS GMP102-Ref-Code 
  https://github.com/GlobalMEMS/GMP102-Ref-Code
"""

from machine import I2C,delay,LED
from machine import Switch   #Get button KEY library
import math
import ustruct as struct

GMP102_ADDR = 0x6C  #SA0 connect to GND
# GMP102_ADDR = 0x6D  #SA0 connect to VIO

# Registers Address
GMP102_REG_RESET   = 0x00
SW_RST_SET_VALUE   = 0x24 # Soft reset 

GMP102_REG_PID     = 0x01

GMP102_REG_STATUS  = 0x02
STATUS_DRDY        = 0x01

GMP102_REG_PRESSH  = 0x06
GMP102_REG_PRESSM  = 0x07
GMP102_REG_PRESSL  = 0x08
GMP102_REG_TEMPH   = 0x09
GMP102_REG_TEMPL   = 0x0A

GMP102_REG_CMD     = 0x30
T_Forced_mode      = 0x08
P_Forced_mode      = 0x09

GMP102_REG_CONFIG1 = 0xA5
RAW_TEMP  = 0x00
RAW_PRESS = 0x02

GMP102_REG_CONFIG2 = 0xA6
OSR_256   = 0x04  # Ultra low power mode
OSR_512   = 0x05
OSR_1024  = 0x00  # Low power mode
OSR_2048  = 0x01
OSR_4096  = 0x02  # Standard resolution
OSR_8192  = 0x03  # High resolution
OSR_16384 = 0x06
OSR_32768 = 0x07  # Ultra high resolution

GMP102_REG_CALIB00  = 0xAA  # Total calibration register count: AAh~BBh total 18
GMP102_CALIBRATION_REGISTER_COUNT = 18
GMP102_CALIBRATION_PARAMETER_COUNT = 9 #(GMP102_CALIBRATION_REGISTER_COUNT/2)

GMP102_TEMPERATURE_SENSITIVITY = 256.00  # 1 Celsius = 256 code
GMP102_CALIB_SCALE_FACTOR = [1.0,1.0e-5,1.0e-10,1.0e-05,1.0e-10,1.0e-15,1.0e-12,1.0e-17,1.0e-21]
fp_base_sea_level_Pa = 101325

def GMP102_init(i2c_bus):
  calib_data = bytearray(GMP102_CALIBRATION_REGISTER_COUNT) 
  fCalibParam = [0] * GMP102_CALIBRATION_PARAMETER_COUNT
  i2c_bus.send(bytearray([GMP102_REG_RESET,SW_RST_SET_VALUE]),GMP102_ADDR)

  delay(100)  # Wait 100ms for reset complete
  # GMP102 get the pressure calibration parameters
  i2c_bus.send(GMP102_REG_CALIB00,GMP102_ADDR)
  i2c_bus.recv(calib_data,GMP102_ADDR)
  # print("".join("\\x%02x" % i for i in calib_data))

  # GMP102 get the pressure calibration parameters
  for i in range(0,9):
    fCalibParam[i] = ((struct.unpack('>h',calib_data[i*2:i*2+2]))[0]/4) * math.pow(10,calib_data[(i*2)+1] & 3 )* GMP102_CALIB_SCALE_FACTOR[i]

  i2c_bus.send(bytearray([GMP102_REG_CALIB00,0x00,0x00,0x00,0x00]),GMP102_ADDR)
  i2c_bus.send(bytearray([GMP102_REG_CONFIG2,0x18|OSR_8192]),GMP102_ADDR)

  return fCalibParam

def GP102_DATA_Ready(i2c_bus):
  status_data = bytearray(1)
  i2c_bus.send(GMP102_REG_STATUS,GMP102_ADDR)
  i2c_bus.recv(status_data,GMP102_ADDR)
  if (status_data[0]&STATUS_DRDY) == 0x01:
    return True
  else :
    return False

def GMP102_PRESSURE_READ(i2c_bus):
  press_data = bytearray(3)
  i2c_bus.send(bytearray([GMP102_REG_CONFIG1,RAW_PRESS]),GMP102_ADDR)
  i2c_bus.send(bytearray([GMP102_REG_CMD,P_Forced_mode]),GMP102_ADDR)

  while GP102_DATA_Ready (i2c_bus) != True :
     pass
  i2c_bus.send(GMP102_REG_PRESSH,GMP102_ADDR)
  i2c_bus.recv(press_data, GMP102_ADDR)
  # print("".join("\\x%02x" % i for i in press_data))
  data = list(press_data)
  data.insert (0,0)
  return(struct.unpack('>i',bytearray(data))[0])

def GMP102_TEMP_READ(i2c_bus):
  temp_data = bytearray(2)
  data = 0
  i2c_bus.send(bytearray([GMP102_REG_CONFIG1,RAW_TEMP]),GMP102_ADDR)
  i2c_bus.send(bytearray([GMP102_REG_CMD,T_Forced_mode]),GMP102_ADDR)

  while GP102_DATA_Ready (i2c_bus) != True :
     pass
  i2c_bus.send(GMP102_REG_TEMPH,GMP102_ADDR)
  i2c_bus.recv(temp_data, GMP102_ADDR)
  # print("".join("\\x%02x" % i for i in temp_data))
  data = struct.unpack('>h',temp_data)
  return(data[0])

# Start Function
if __name__ == '__main__':
  p = [0]*9
  KeyA = Switch('keya')    #Create button A
  led = LED('ledg')
  led.off()

  GMP102_i2c = I2C(0,I2C.MASTER,baudrate=100000)     #Create I2C0 Master Mode, Baudrate=100kHz
  p = GMP102_init(GMP102_i2c)
  
  while True:
    led.on()
    press_raw=GMP102_PRESSURE_READ(GMP102_i2c)
    temp_raw=GMP102_TEMP_READ(GMP102_i2c)
    led.off()
  
    temp = temp_raw / GMP102_TEMPERATURE_SENSITIVITY

    # 100 Pa = 1 millibar (Pa = newton per square meter)
    fP_Pa =p[0] + \
           p[1]*temp_raw + \
           p[2]*temp_raw**2 + \
           p[3]*press_raw + \
           p[4]*temp_raw*press_raw + \
           p[5]*(temp_raw**2)*press_raw + \
           p[6]*math.pow(press_raw,2) + \
           p[7]*temp_raw*math.pow(press_raw,2) + \
           p[8]*math.pow(temp_raw,2)*math.pow(press_raw,2)

    # Pressure altitude conversion
    #      See https://en.wikipedia.org/wiki/Pressure_altitude
    altm = float(44307.694 *(1-(math.pow((fP_Pa/fp_base_sea_level_Pa),0.190284))))
  
    print ('Temperature={:.2f}*C\nPressure={:.2f}Pa\nApprox Altitude={:3.2f}m'.format(temp,fP_Pa,altm))
    if KeyA.value() == True:      #Press A Key
      break
    delay(1000)
  
  GMP102_i2c.deinit()
