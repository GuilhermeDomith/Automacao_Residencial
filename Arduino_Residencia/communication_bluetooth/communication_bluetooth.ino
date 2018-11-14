char data = 0;
int LED = 13;

void setup() {
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
}

void loop() {

  if(Serial.available() > 0) {

    data = Serial.read();      //Read the incoming data and store it into variable data
    Serial.print(data);        //Print Value inside data in Serial monitor
    Serial.print("\n");        //New line

    if(data == '1')            //Checks whether value of data is equal to 1
      digitalWrite(LED, HIGH);  //If value is 1 then LED turns ON
    else if(data == '0')       //Checks whether value of data is equal to 0
      digitalWrite(LED, LOW);   //If value is 0 then LED turns OFF
  }

}
