from hcsr04 import HCSR04
from machine import delay,Switch

sonar = HCSR04()
keyA = Switch('keya')
while True:
    if keyA :
        distance = round(sonar.distance_mm()/10)
        if distance < 10:
            print(str(distance))
        else:
            print('x',str(distance))
        
    delay(100)
	