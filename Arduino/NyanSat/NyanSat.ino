/* 
All helper functions will be merged into (this) one Arduino Sketch file, beucase I can't figure out a way to have helper functions on separate files
Maybe I'll separate them later.

Project Hermes (Internal Tracker: NyanSat)
*/

// Importing libraries
#include "DataModels.h"
#include <Adafruit_BMP280.h>
#include <Adafruit_SI1145.h>

Adafruit_BMP280 bmp;
Adafruit_SI1145 uv = Adafruit_SI1145();

// Both of these Adafruit classes seems to use the same "Wire" object? Should I create them here and pass it in as a parameter?

SensorData collectSensorData() {
  /* Collects sensor data from all connected sensors and processes them / Recolecta datos de cada sensor y los procesa */
  // Skeleton / Esqueleto
  SensorData currentSensorData;
  
  // Onboard timer / temporizador
  currentSensorData.time = millis();
  
  // BMP280: Temperature, pressure / BMP280: Temperatura, presión
  currentSensorData.temperature = bmp.readTemperature();
  currentSensorData.pressure = bmp.readPressure();
  
  // SI1145
  currentSensorData.visibleLight = uv.readVisible();
  currentSensorData.infraredLight = uv.readIR();
  currentSensorData.UVIndex = uv.readUV() / 100.0;
  return currentSensorData;
}

void setup() {
  /* Initialize Remote Transmission */
  Serial.begin(9600);

  /* Sensor Setup */
  // BMP280
  bmp.begin();
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
  // SI1145
  uv.begin();

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
