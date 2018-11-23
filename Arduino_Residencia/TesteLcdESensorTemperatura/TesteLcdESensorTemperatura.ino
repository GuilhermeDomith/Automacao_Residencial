//Programa: Teste de Display LCD 16 x 2


//Carrega a biblioteca LiquidCrystal
#include <LiquidCrystal.h>

#include "LM35.h"
 
//Define os pinos que serão utilizados para ligação ao display
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);


const int pinoLM35 = A0; // Define o pino que lera a saída do LM35
float temperatura; // Variável que armazenará a temperatura medida

byte graus[8] = { B01110, B01010, B01010,  B001110, B00000, B00000, B00000, B00000}; 

LM35 sensor(pinoLM35);
 
void setup(){
  //Define o número de colunas e linhas do LCD
  lcd.begin(16, 2);
  lcd.createChar(1, graus);
  Serial.begin(9600); // inicializa a comunicação serial
}
 
void loop(){
 
  
  temperatura = (float(analogRead(pinoLM35))*5/(1023))/0.01;;
  Serial.println(temperatura);

  int rawvoltage = analogRead(pinoLM35);
  
  float millivolts = (rawvoltage/1024.0) * 5000;
  float celsius = millivolts/10;
 
  //Serial.print("Temperatura: ");
  //Serial.println(temperatura);
  //delay(2000);
  //Limpa a tela
  lcd.clear();
  //Posiciona o cursor na coluna 3, linha 0;
  lcd.setCursor(2, 0);
  //Envia o texto entre aspas para o LCD
  lcd.print(String(temperatura) + " ");
  lcd.write(1);
  lcd.print("C");
  lcd.setCursor(0, 1);
  lcd.print(" LCD 16x2");
  delay(2000);
   
 /* //Rolagem para a esquerda
  for (int posicao = 0; posicao < 3; posicao++)
  {
    lcd.scrollDisplayLeft();
    delay(300);
  }
   
  //Rolagem para a direita
  for (int posicao = 0; posicao < 6; posicao++)
  {
    lcd.scrollDisplayRight();
    delay(300);
  }*/
}
