#include <SoftwareSerial.h>
#include <string.h>
#include <Ultrasonic.h>
 

//Define os pinos para o trigger e echo
#define pino_trigger 3
#define pino_echo 2

#define ALARME 6
#define DISTANCIA 8.50
#define COMP_LED 1
#define COMP_VEN 2

bool state = false;
bool alarmeAtivado = false;
bool movimentoDetectado = false;

int statusLeds[] = {0, 0, 0, 0};
int pinosLeds[] = {13, 12, 8, 7};
char codigo[3];
bool requisicaoRecebida = false;
 
SoftwareSerial serial1(11,10);
Ultrasonic ultrasonic(pino_trigger, pino_echo);

void setup() {
  serial1.begin(9600);
  Serial.begin(9600);
  definirPinosComoSaida();
  pinMode(ALARME,OUTPUT);
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
  alarme();
  delay(2000);

}

void verificarCodigo(){
  String mensagem = "", numero;

  if(codigo[0] == 'L' || codigo[0] == 'l'){
    String indiceString;
    indiceString.concat(codigo[1]);
    int indice = indiceString.toInt();

    if(codigo[2] == '1'){
      alterarStatusLed(indice, true); 
    }else{
      alterarStatusLed(indice, false);
    }    
  }

  else{
    if(codigo[0] == 'A' || codigo[0] == 'a'){
      if(codigo[1] == '1'){
        controlarAlarme(true);
      }else{
        controlarAlarme(false);
      }
    }
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

void definirPinosComoSaida(){
  int i = 0;
  
  for(i = 0; i < 4; i++) {
    pinMode(pinosLeds[i], OUTPUT);
  }
}

void controlarAlarme(bool ativar){
    Serial.println("Ativar alarme");
    alarmeAtivado = ativar;
}
void alarme(){
  float cmMsec, inMsec;
  long microsec = ultrasonic.timing();
  cmMsec = ultrasonic.convert(microsec, Ultrasonic::CM);
  inMsec = ultrasonic.convert(microsec, Ultrasonic::IN);

  if(alarmeAtivado){
    if(!movimentoDetectado){
      if(cmMsec <= DISTANCIA){
        movimentoDetectado = true;
      }
  }else
    digitalWrite(ALARME,LOW);
  }  

  if(movimentoDetectado){
    digitalWrite(ALARME, HIGH);
  }
}
