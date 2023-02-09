/* 
Bilingual Project, comments and documentation would be in both languages / Proyecto bilingüe, comentarios y documentaciones estarán disponibles en ambos lenguajes

All helper functions will be merged into (this) one Arduino Sketch file, beucase I can't figure out a way to have helper functions on separate files
Maybe I'll separate them later.
Todos los funciones secundarios estarán dentro de este archivo de Arduino Sketch, porque no encuentro ninguna forma se separarlos en archivos diferentes
Lo dejaré como una tarea para el futuro.

Project/Proyecto Hermes (Internal Tracker: NyanSat)
*/

// Importing libraries / Importación de librerías
#include "DataModels.h"
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp;

SensorData collectSensorData() {
  // Collects sensor data from all connected sensors and processes them / Recolecta datos de cada sensor y los procesa
  SensorData currentSensorData;
  currentSensorData.time = millis();
  
  currentSensorData.temperature = bmp.readTemperature();
  currentSensorData.pressure = bmp.readPressure();
  
  return currentSensorData;
}

void setup() {
  Serial.begin(9600);
  bmp.begin();
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
}

void loop() {
  // Timer here, please / Timer aquí porfa
  
  SensorData s_data = collectSensorData();
  Serial.print(s_data.time);
  Serial.print(", ");
  Serial.print(s_data.pressure);
  Serial.print(", ");
  Serial.print(s_data.temperature);
  Serial.println("");
  
  delay(1000);
}
