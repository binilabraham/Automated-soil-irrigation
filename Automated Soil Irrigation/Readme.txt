#Working
Initially switch input will be low and now the system functions as an automatic system. 
The moisture sensor will sense the readings and the LCD displays the corresponding readings 
and if the readings is greater than the threshold value then the relay will pin will go high
and hence the pump get started. If the reading go less than the lower threshold then the relay
pin will go low an hence the pump will get off. If the switch is pressed then the switch pin will
input a high state to the arduino and then system starts to functions Bluetooth mode. In Bluetooth
mode the corresponding readings of the moisture will be shown in the android to which the Bluetooth
module is paired. If a command ‘n’ is given from the app to the arduino then the relay pin will be
set high and the pump starts and if a command ‘f’ is given from the app to the arduino then the relay
pin will be set low and the pump turns-off. If a command ‘c’ is given from the  app to the arduino then
the system will switch mode of operation  from Bluetooth to automatic mode. The buzzer pin will be set high
for few seconds when the relay pin is high and in Bluetooth it acts as an alert to the user to get when the 
pump to be turned off and on. 
