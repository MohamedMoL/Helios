/*
   PROGRAMA DE PRUEBA: APC220
   CONEXION:
             RXD: Arduino Pin 1
             TXD: Arduino Pin 0
             GND: Arduino GND
             VCC: Arduino 5V
             
   Autor: Renato H.
   http://beetlecraft.blogspot.pe/
  
   El siguiente programa es de uso publico, cualquier modificacion o mal uso del mismo que pudiera ocasionar el mal funcionamiento de la plataforma de uso de la misma no es responsabilidad del autor
*/

#include <SoftwareSerial.h>

SoftwareSerial radio(8, 9); // Pin2: RX， Pin3: TX

void setup(){
  Serial.begin(9600); // Velocidad de comunicacion
                      // La velocidad del puerto serial debe ser
                      // la misma que la de configuracion del modulo
  Serial.println("USB Serial initialized");
  radio.begin(9600);
  Serial.println("Radio initialized");
}

void loop(){
 radio.println("Radio: Hola mundo"); // Mensaje "Hola mundo"
 Serial.println("USB Serial: Hola mundo");
 delay(1000);                  // Retraso de envio cada 1 segundo
}
