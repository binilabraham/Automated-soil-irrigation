#include <SoftwareSerial.h> //Software Serial Port
#include <LiquidCrystal.h> // include the library code
#define RxD 6 // This is the pin that the Bluetooth (BT_TX) will transmit to the Arduino (RxD)
#define TxD 7 // This is the pin that the Bluetooth (BT_RX) will receive from the Arduino (TxD)
#define lothreshold 600 // Defining Thresholds
#define upthreshold 900//
#define DEBUG_ENABLED 1//
SoftwareSerial blueToothSerial(RxD,TxD);//
int plantSensor=A0; // sensor pins
int value=0;  //initializing sensor value & variables
int pump=8; // water pump control pin
int buf=10;
LiquidCrystal lcd(12,11,5,4,3,2); // initialize the library with the numbers of the interface pins
const int buttonPin=9;//
int buttonState=0;// variable for reading the pushbutton status
void watering();//
void setup()
{
  Serial.begin(9600);//
  pinMode(RxD,INPUT); // Setup the Arduino to receive INPUT from the bluetooth shield on Digital Pin 6   
  pinMode(TxD,OUTPUT); // Setup the Arduino to send data (OUTPUT) to the bluetooth shield on Digital Pin 7
  setupBlueToothConnection(); //Used to initialise the Bluetooth shield
  pinMode(pump,OUTPUT);//
  pinMode(buf,OUTPUT);
  pinMode(buttonPin,INPUT);//
  lcd.begin(16,2); // set up the LCD's number of columns and rows:
  digitalWrite(pump,LOW); //pump off at initial
}

void loop()
{ char recvChar;
  int f=0;
  buttonState=digitalRead(buttonPin); // read the state of the pushbutton value:
  value=analogRead(plantSensor); //Reading values from sensor
  if(buttonState==HIGH) 
   { 
     while(1)
      {                                                                                                                                                            
         if(blueToothSerial.available())//check if there's any data sent from the remote bluetooth shield
           {
             Serial.println("bluetooth");
             //if(blueToothSerial.read()!='0')
              
             recvChar=blueToothSerial.read();
             
             blueToothSerial.print("\n        Reading=  ");
             blueToothSerial.print(value);
             Serial.print(recvChar); // Print the character received to the Serial Monitor (if required)
             lcd.clear();
             lcd.setCursor(0,1);
             lcd.print("\nbluetooth");
             delay(1000);
             lcd.clear();
             lcd.setCursor(0,1);
             lcd.print("\nReading=");
             lcd.print(value); // Print a message to the LCD.
             delay(2000);
              
             if(value>=lothreshold)
              { digitalWrite(buf, HIGH); //buzzer on
                delay(1000);
                digitalWrite(buf, LOW); //buzzer off
                
                 blueToothSerial.print("\n         LOW");
                 blueToothSerial.print("\n        ON PUMP\n");
              }
            
             if(recvChar=='n')//If the character received = 'r' , then change the RGB led to display a RED colour
             {
                 digitalWrite(pump, HIGH); //Pump onn
                 
              }
             
             if(value<=upthreshold)
              { 
                digitalWrite(buf, HIGH); //BUZZER ON
                delay(2000);
                digitalWrite(buf, LOW); //buzzer off
                 blueToothSerial.print("\nHIGH");
                 blueToothSerial.print("\nOFF PUMP");
              }
             
             if(recvChar=='f')
              {
                
                digitalWrite(pump, LOW); //Pump off
                delay(3000); //Wait till extra water flows out 
              }
             
             if(recvChar=='c')
              { f=1;
                break;
              }
              delay(2500);
             value=analogRead(plantSensor); 
             blueToothSerial.print("\n        Reading=  ");
             blueToothSerial.print(value);
             Serial.print(recvChar); // Print the character received to the Serial Monitor (if required)
             lcd.clear();
             lcd.setCursor(0,1);
             lcd.print("\nbluetooth");
             lcd.clear();
             lcd.setCursor(0,1);
             lcd.print("\nReading=");
             lcd.print(value); // Print a message to the LCD.
             
           }
         if(f==1)
          {
             break;
          }
       }
     }
  else
   {
    Serial.println("Automatic");
    value=analogRead(plantSensor); //Reading values from sensor
    Serial.println(value);  //Displaying values on serial monitor for debugging
    lcd.clear();          
    lcd.setCursor(0,1);
    lcd.print("Reading=");
    lcd.print(value); // Print a message to the LCD.
    delay(1000);
    lcd.clear();
    delay(2000);
    
    if(value>=lothreshold)
     {
      watering();  //control watering operations
      delay(2000);
     }
    
     value=analogRead(plantSensor);
     lcd.clear();
     lcd.setCursor(0,1);
     lcd.print("Reading=");
     lcd.print(value); // Print a message to the LCD.
     delay(1000);
     lcd.clear();
     delay(2000);
     
     if(value<=upthreshold)
     {
      digitalWrite(pump,LOW); //Pump off
       
     }
   } 
      
}

void watering()
{ digitalWrite(buf, HIGH); //Buzzer On
  delay(1000);
  digitalWrite(buf, LOW);
  Serial.println("Watering  Plant");
  lcd.clear();
  lcd.setCursor(0,1);
  lcd.print("Watering");// Print a message to the LCD.
  lcd.print(" Plant");
  delay(1000);
  lcd.clear();
  digitalWrite(pump,HIGH); //Pump onn
  delay(2000);

}

//setup the bluetooth shield
void setupBlueToothConnection()
{
 blueToothSerial.begin(9600); //Set BluetoothBee BaudRate to default baud rate 9600
 blueToothSerial.print("\r\n+STWMOD=0\r\n"); //set the bluetooth work in slave mode
 blueToothSerial.print("\r\n+STNA=SeeedBTSlave\r\n"); //set the bluetooth name as "SeeedBTSlave"
 blueToothSerial.print("\r\n+STOAUT=1\r\n"); // Permit Paired device to connect me
 blueToothSerial.print("\r\n+STAUTO=0\r\n"); // Auto-connection should be forbidden here
 delay(2000); // This delay is required.
 blueToothSerial.print("\r\n+INQ=1\r\n"); //make the slave bluetooth inquirable 
 Serial.println("The slave bluetooth is inquirable!");
 delay(2000); // This delay is required.
 blueToothSerial.flush();
}
