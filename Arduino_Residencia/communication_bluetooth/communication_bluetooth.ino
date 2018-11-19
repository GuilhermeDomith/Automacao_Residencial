#include <SoftwareSerial.h>
#include <string.h>

#define COMP_LED 1
#define COMP_VEN 2

int LED = 13;
bool state = false;

int statusLeds[] = {0, 0, 0, 0};
int pinosLeds[] = {13, 14, 15, 16};
char codigo[3];
bool requisicaoRecebida = false;
 
SoftwareSerial serial1(11,10);

void setup() {
  serial1.begin(9600);
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
}

void loop() {
  char caracter;
  limpaArrayCodigo();


  int contador = 0;


  while(serial1.available() > 0) {
    caracter = serial1.read();
    codigo[contador] = caracter;
    contador++;   
  }

  if(codigo[0] != '0'){
    verificarCodigo();
  }
  controlarLeds();
  delay(2000);

}

void executarAcao(){
  if(codigo[0] == 'l' || codigo[0] == 'L'){
     
  }

  
}

void verificarCodigo(){
  String mensagem = "", numero;

  if(codigo[2] == '1'){
    mensagem.concat("Acender/ligar o ");
    alterarStatusLed(0, true); 
  }else{
    alterarStatusLed(0, false);
  }

  if(codigo[0] == 'L' || codigo[0] == 'l'){
    mensagem.concat("LED "); 
  }

  mensagem.concat(codigo[1]);

  numero += codigo[1];
  int n =  numero.toInt();

  if(n == 1){
    Serial.println("Acenda o led.");
  }

  
  Serial.println(mensagem);
  

  
}


void alterarStatusLed(int indiceLed, bool acender){
  if(acender == true){
    statusLeds[indiceLed] = 1;
  }else{
    statusLeds[indiceLed] = 0;
  }
}

void controlarLeds(){
  int i = 0;
  
  for(i = 0; i < 4; i++){
    digitalWrite(pinosLeds[i], statusLeds[i]);
  }
}

void limpaArrayCodigo(){
    codigo[0] = '0';
    codigo[1] = '0';
    codigo[2] = '0';
}
