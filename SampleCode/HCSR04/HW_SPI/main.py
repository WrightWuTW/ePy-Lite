import utime as time
from dht import DHT11, InvalidChecksum
from machine import Pin

while True:
    time.sleep(1)
    pin = Pin(Pin.board.P3, Pin.OUT, Pin.PULL_DOWN)
    sensor = DHT11(pin)
    t  = sensor.temperature()
    h = sensor.humidity()
    print("Temperature: {}".format(sensor.temperature))
    print("Humidity: {}".format(sensor.humidity))
    
    time.sleep(1)
