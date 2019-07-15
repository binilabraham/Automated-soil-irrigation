from nanpy import (ArduinoApi, SerialManager)
from time import sleep
import math

batMonPin = 14
val = 0
pinVoltage = 0
BatteryVolatge = 0

try:
    connection = SerialManager()
    a = ArduinoApi (connection = connection)
except:
    print("failed to connect to Arduino")
    
a.pinMode(batMonPin, a.INPUT)

try:
    while True:
        val = a.analogRead(batMonPin)
        print(a.analogRead(batMonPin))
        pinVolatge = (val * 0.0020283)
        batteryVoltage = (pinVolatge * 60.992) 
        print ("Our Total is: {}".format(batteryVoltage))
        sleep(1)
        

except:
    print ("Check man")
