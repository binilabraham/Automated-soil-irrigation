from nanpy import (ArduinoApi, SerialManager)
from time import sleep
import math

PinVClamp = 14   #Sensor SCT-013-000 port A0
PinVirtGND = 15   # A1 <span id="result_box" class="" lang="en"><span class="hps">Virtual</span> <span class="hps alt-edited">ground</span></spa

numReadings = 300 #samples to calculate Vrms.

readingsVClamp=[0]*300    # samples of the sensor SCT-013-000

readingsGND=[0]*300      # samples of the <span id="result_box" class="" lang="en"><span class="hps">virtual</span> <span class="hps alt-edited">ground</span></span>

SumSqGND = 0            
SumSqVClamp = 0
total = 0
totalI = 0


try:
    connection = SerialManager()
    a = ArduinoApi (connection = connection)
except:
    print("failed to connect to Arduino")
    
a.pinMode(PinVClamp, a.INPUT)
a.pinMode(PinVirtGND, a.INPUT)

 
'''try:
    for x in range(0,199):
        readingsVClamp.append(0)
        readingsGND.append(0)
        print ("Our button State is: {}".format(readingVclamp[x]))
except:
    print("Unable to clear sampling space") '''
 
try:
    while True:
        SumSqGND = 0
        SumSqVClamp = 0
        total = 0
        totalI = 0
        sleep(1)
        for i in range(300):
            #print (i)
            #if (a.analogRead(PinVClamp)>512) && (a.analogRead(PinVClamp)<516):
            readingsVClamp[i] = a.analogRead(PinVClamp) - a.analogRead(PinVirtGND)
                
            #readingsVClamp[i] = a.analogRead(PinVClamp) - 515
            #print(i)
            #print(a.analogRead(PinVirtGND))
            #print(a.analogRead(PinVClamp))
            sleep(0.1)
            

  
 
    #Calculate Vrms
        for i in range(300):
            SumSqVClamp = SumSqVClamp + math.pow(readingsVClamp[i],2)
            #print(SumSqVClamp)
            #print"%f" %(SumsqVclamp)
            #print"%f" %(numReadings)
            total = math.sqrt(SumSqVClamp/300)
        print(total)
            
        total = ((total* 0.076)-0.076) # Rburden=330 ohms, LBS= 0,004882 V (5/1024)
                          # Transformer of 2000 laps (SCT-013-000).
                          # 5*120*2000/(330*1024)= 2/3 (aprox)
        print ("Our Total is: {}".format(total))
        sleep(1.5)

except:
    print ("Check man")
