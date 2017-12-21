#include "DHT.h"
#include <Timer.h> 
#define DHTPIN 2    
#define DHTTYPE DHT11   

int sensorValue =0;
int Key1pin =3;
int ledpin1 =13;

DHT dht(DHTPIN, DHTTYPE); // Initialize DHT sensor
void setup(){
Serial.begin(9600);
delay(300); //Let system settle
Serial.println("組合測試\n\n\n\n");
delay(700); //Wait rest of 1000ms recommended delay before
 //accessing sensor

pinMode(5, OUTPUT);

}

void loop(){

int soil_wet = analogRead(0) ;
  Serial.print("土壤感測器:");
  Serial.print( soil_wet );
int keystate = digitalRead(Key1pin);
  if(keystate == 1){
    Serial.print("  not detect");
    digitalWrite(ledpin1,LOW);
  }
  else{
    Serial.print("  detected");
    digitalWrite(ledpin1,HIGH);
  }
  Serial.println("  ");
  delay(1000);
  
  if (soil_wet > 200)
  {
    digitalWrite(6, HIGH);
  } 
  else
  {
    digitalWrite(6, LOW);
  }
  
  delay(2000);
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float f = dht.readTemperature(true);
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
    }
  Serial.print("空氣濕度: ");
  Serial.print(h);
  Serial.print("%\t");
  Serial.print("溫度: ");
  Serial.print(t);
  Serial.print("*C\t");

if(t>25) //如果溫度大於25度
{ 
 digitalWrite(5, LOW ); //pin5 將顯示Low 
 Serial.println("*PIN 0");
}
else
{
 digitalWrite(5,HIGH); //若否，pin5 將顯示 High
  Serial.println("*PIN 1");
}


}