#include <SoftwareSerial.h>
#include <string.h>

int LED = 13;
bool state = false;

SoftwareSerial serial1(11,10);

void setup() {
  serial1.begin(9600);
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
}

void loop() {
  char caracter;

  if(state == true){
    digitalWrite(LED, HIGH);
  }else{
    digitalWrite(LED, LOW);
  }


  if(serial1.available()) {
    caracter = serial1.read();      //Read the incoming data and store it into variable data
    Serial.print(caracter);        //Print Value inside data in Serial monitor
    Serial.print("\n");        //New line

    if(caracter == 'A')   {         //Checks whether value of data is equal to 1
      state = true;
      
    }
    else    //Checks whether value of data is equal to 0
      state = false;
  }

}
