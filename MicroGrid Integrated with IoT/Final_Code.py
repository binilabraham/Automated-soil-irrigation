from nanpy import (ArduinoApi, SerialManager)
from time import sleep
import math
import datetime 
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

#set the pins in Raspberry and Arduino
#Raspberry

Relay_1 = 25 #Relay for Inverter Supply 
Relay_2 = 24 #Relay for Main Supply

#Arduino

PinVClamp_B = 14    #Sensor SCT-013-000 port A0
PinVirtGND_B = 15   #port A1
PinVClamp_S = 16    #Sensor SCT-013-000 port A2
PinVirtGND_S = 17   #port A3
batMonPin = 18      #Battery Monitor port A4

#Setting variables
readingsVClamp_B = [0]*300
readingsVClamp_S = [0]*300
readingsGND = [0]*300
SumSqGND = 0
SumSqVClamp = 0
Total = 0
val=0
Current_B = 0
Current_S = 0
Battery = 0

#Set the GPIO ports as output 
GPIO.setup(Relay_1, GPIO.OUT)
GPIO.setup(Relay_2, GPIO.OUT)

#Arduino Connection Check
try:
    connection = SerialManager()
    a = ArduinoApi (connection = connection)
except:
    print("failed to connect to Arduino")

#set the Analog pins of Arduino as Input     
a.pinMode(PinVClamp_B, a.INPUT)
a.pinMode(PinVirtGND_B, a.INPUT)
a.pinMode(PinVClamp_S, a.INPUT)
a.pinMode(PinVirtGND_S, a.INPUT)
a.pinMode(batMonPin, a.INPUT)

def Current_Calc_B():
    SumSqVClamp=0
    total = 0
    for i in range(300):
        readingsVClamp_B[i] = a.analogRead(PinVClamp_B) - a.analogRead(PinVirtGND_B)
        #sleep(0.1)

    for i in range(300):
        SumSqVClamp = SumSqVClamp + math.pow(readingsVClamp_B[i],2)
    total = math.sqrt(SumSqVClamp/300)
    total = ((total*0.076)-0.076)
    return total


def Current_Calc_S():
    SumSqGND = 0
    SumSqVClamp = 0
    total = 0
    for i in range(300):
        readingsVClamp_S[i]= a.analogRead(PinVClamp_S) - a.analogRead(PinVirtGND_S)
        #sleep(0.1)
    #Calculate Vrms
    for i in range(300):
        SumSqVClamp = SumSqVClamp + math.pow(readingsVClamp_S[i],2)
    total = math.sqrt(SumSqVClamp/300)
    total = ((total*0.076)-0.076)
    return total

def Battery_Test():
    val=0
    for i in range(10):
        val = val + a.analogRead(batMonPin)
        sleep(0.1)
    val = (val/10)
    pinVoltage = (val*0.0048)
    batteryVoltage = (pinVoltage * 2.77335878)
    return batteryVoltage

def File_Write(current1,current2,voltage):
	#CurrentDT = datetime.datetime.now()
	CurrentDT = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	f = open("readings.log", "a")
	#writelist_DATE = [CurrentDT.year,CurrentDT.month,CurrentDT.day,CurrentDT.hour,CurrentDT.minute,CurrentDT.second]
	writelist_Value = [current1,current2,voltage]
	#for variable in writelist_DATE:
	f.write(CurrentDT)
	f.write(" ")
	for variable in writelist_Value:
	    f.write(str(variable))
	    f.write(" ")
	f.write("\n")
	f.close()	

try:
	#f = open("Readings.txt","a+w")
	#f.close()
	while True:
            Current_B = 0
            Current_S = 0
            Battery = 0
            Current_B = Current_Calc_B()
            Current_S = Current_Calc_S()
            Battery = Battery_Test()
            File_Write(Current_B, Current_S, Battery)
            if (Current_B > 4) or (Battery < 11.6):
                GPIO.output(Relay_1,GPIO.LOW)
                GPIO.output(Relay_2,GPIO.LOW)
            else:
                GPIO.output(Relay_1,GPIO.HIGH)
                GPIO.output(Relay_2,GPIO.HIGH)
		

except KeyboardInterrupt:
    pass
finally:
    print("Bye")
    GPIO.cleanup()
