#include <SoftwareSerial.h>
#include <string.h>
#include <Ultrasonic.h>
 

//Define os pinos para o trigger e echo
#define pino_trigger 3
#define pino_echo 2

#define ALARME 6
#define LUM A0
#define DISTANCIA 10
#define COMP_LED 1
#define COMP_VEN 2

bool state = false;
bool alarmeAtivado = false;
bool movimentoDetectado = false;
bool modoAutomatico = false;

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
  
  
  alarme();

  if(modoAutomatico){
    iluminacaoModoAutomatico();  
  }else{
    controlarLeds();
  }
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
    }else{
      if(codigo[0] == 'M' || codigo[0] == 'm'){
        if(codigo[1] == '1'){
          modoAutomatico = true;
        }else{
          modoAutomatico = false;
        }
      }
    }
  }
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
    alarmeAtivado = ativar;
    if(!ativar)
      movimentoDetectado = false;
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

  if(movimentoDetectado && alarmeAtivado){
    digitalWrite(ALARME, HIGH);
  }else{
    digitalWrite(ALARME, LOW);
  }
}


void iluminacaoModoAutomatico(){
  int ldrValor = 0;
  
  ldrValor = analogRead(LUM); //O valor lido será entre 0 e 1023
 
 //se o valor lido for maior que 500, liga o led
 if (ldrValor>= 700){
  digitalWrite(pinosLeds[0], HIGH);
 }else{
  digitalWrite(pinosLeds[0], LOW);
 }
 
 //imprime o valor lido do LDR no monitor serial
 Serial.println(ldrValor);
}
