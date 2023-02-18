#include <Servo.h>

//Teensy 4.0 being used
Servo xservo;
Servo yservo;

#define PUMP_PIN 10
#define LED_BLUE 5
#define LED_RED 3
#define LED_GREEN 0
#define BRIGHTNESS 50

int servoByte = 0;
void setup() {
  // put your setup code here, to run once:

  xservo.attach(22);
  yservo.attach(21);
  pinMode(LED_BLUE, OUTPUT);
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(PUMP_PIN, OUTPUT);
  digitalWrite(LED_BLUE, LOW);
  digitalWrite(LED_RED, LOW);
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(PUMP_PIN, LOW);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  for (int i = 0; i < Serial.available(); i++) {
    int incomingbyte = Serial.read();
    if (servoByte == 0) {
      if (incomingbyte == 65) {
        digitalWrite(PUMP_PIN, HIGH);
        //Serial.write("Pump turned on \n");
      } else if (incomingbyte == 66) {
        digitalWrite(PUMP_PIN, LOW);
        //Serial.write("Pump turned off \n");
      } else if (incomingbyte == 67) {
        analogWrite(LED_RED, BRIGHTNESS);
        //Serial.write("Red LED turned on \n");
      } else if (incomingbyte == 68) {
        analogWrite(LED_RED, 0);
        //Serial.write("Red LED turned off");
      } else if (incomingbyte == 69) {
        analogWrite(LED_GREEN, BRIGHTNESS);
        //Serial.write("Green LED turned on \n");
      } else if (incomingbyte == 70) {
        analogWrite(LED_GREEN, 0);
        //Serial.write("Green LED turned off");
      } else if (incomingbyte == 71) {
        analogWrite(LED_BLUE, BRIGHTNESS);
        //Serial.write("Blue LED turned on");
      } else if (incomingbyte == 72) {
        analogWrite(LED_BLUE, 0);
        //Serial.write("Blue LED turned off");
      } else if (incomingbyte == 73) {
        servoByte = 1;
        //Serial.write("Awaiting byte for X servo");
      } else if (incomingbyte == 74) {
        servoByte = 2;
        //Serial.write("Awaiting byte for Y servo");
      }
    }else{
      if(servoByte == 1){
        xservo.write(incomingbyte);
        Serial.write("Set x servo to byte");
      }else if(servoByte == 2){
        yservo.write(incomingbyte);
        Serial.write("Set y servo to byte");
      }
      servoByte = 0;
    }
  }

}
