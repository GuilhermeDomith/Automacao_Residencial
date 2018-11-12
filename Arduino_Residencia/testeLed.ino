// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int led = 2;
int led2 = 3;
// the setup routine runs once when you press reset:
void setup(){
  // initialize the digital pin as an output.
  pinMode(led, OUTPUT);
  pinMode(led2,OUTPUT);
}

// the loop routine runs over and over again forever:
void loop() {
  	acendeLed(1,3);
  	delay(5000);
}
void acendeLed(int status,int id){
  if(status == 1 && id == 2){
  	digitalWrite(led, HIGH);
  	digitalWrite(led2, LOW);
  }
  else{
    digitalWrite(led2, HIGH);
  	digitalWrite(led, LOW);  
  }
	

}