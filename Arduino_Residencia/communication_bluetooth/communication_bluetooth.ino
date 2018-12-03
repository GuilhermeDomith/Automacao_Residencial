#include <SoftwareSerial.h>
#include <string.h>
#include <Ultrasonic.h>
#include <LiquidCrystal.h>
 

//Define os pinos para o trigger e echo
#define pino_trigger 3
#define pino_echo 2

#define ALARME 53
#define LUZ_FORA_1 43
#define LUZ_FORA_2 49
#define LUM A1
#define DISTANCIA 6
#define COMP_LED 1
#define COMP_VEN 2

LiquidCrystal lcd(22, 24, 21, 20, 19, 18);

bool state = false;
bool alarmeAtivado = false;
bool movimentoDetectado = false;
bool modoAutomatico = false;
bool mostrarTemperatura = false;

int statusLeds[] = {0, 0, 0, 0};
int pinosLeds[] = {13, 12, 8, 7};
char codigo[3];
//const int LM35 = A0; // Define o pino que lera a saída do LM35
float temperatura; // Variável que armazenará a temperatura medida
bool requisicaoRecebida = false;
 
SoftwareSerial serial1(11,10);
Ultrasonic ultrasonic(pino_trigger, pino_echo);

void setup() {
  serial1.begin(9600);
  Serial.begin(9600);
  definirPinosComoSaida();
  lcd.begin(16, 2);
  pinMode(ALARME,OUTPUT);
  pinMode(LUZ_FORA_1, OUTPUT);
  pinMode(LUZ_FORA_2, OUTPUT);
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
  }

  controlarLeds();


  controlarLCD();
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
    Serial.println("Entrou alarme");
    digitalWrite(ALARME, HIGH);
  }else{
    digitalWrite(ALARME, LOW);
  }
}


void iluminacaoModoAutomatico(){
  int ldrValor = 0;
  
  ldrValor = analogRead(LUM); //O valor lido será entre 0 e 1023

  Serial.println(ldrValor);
 
 //se o valor lido for maior que 850, liga o led
 if (ldrValor >= 850){
  digitalWrite(LUZ_FORA_1, HIGH);
  digitalWrite(LUZ_FORA_2, HIGH);
 }else{
    digitalWrite(LUZ_FORA_1, LOW);
    digitalWrite(LUZ_FORA_2, LOW);
 }

 Serial.println(ldrValor);
}


void controlarLCD(){
  String alarme = "ALARME: ", modeAtm = "Luz Autm.: ";
  
  if(alarmeAtivado)
    alarme.concat("ON");
  else
    alarme.concat("OFF");

  if(modoAutomatico)
    modeAtm.concat("ON");
  else
    modeAtm.concat("OFF");

  
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(alarme);
  lcd.setCursor(0, 1);
  lcd.print(modeAtm);
}
