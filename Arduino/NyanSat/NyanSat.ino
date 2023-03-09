// Importing libraries
#include "DataModels.h"
#include "CansatConfig.h"
#include <Adafruit_BMP280.h>
#include <Adafruit_SI1145.h>
#include <SoftwareSerial.h>
#include <I2Cdev.h>
#include <MPU6050.h>
#include <TinyGPS++.h>
#include <math.h>
#include <limits.h>
#include <string.h>
#include <AltSoftSerial.h>

TinyGPSPlus gps;

Adafruit_BMP280 bmp;
Adafruit_SI1145 uv = Adafruit_SI1145();
SoftwareSerial gps_serial(GPS_RX, GPS_TX);
AltSoftSerial radio;
MPU6050 accelgyro;

SensorData collectSensorData() {
  /* Collects sensor data from all connected sensors and processes them */
  // Skeleton
  SensorData currentSensorData;
  
  // Onboard timer
  currentSensorData.time = millis();
  
  // BMP280: Temperature, pressure / BMP280: Temperatura, presión
  currentSensorData.temperature = bmp.readTemperature();
  currentSensorData.pressure = bmp.readPressure();

  // MPU6050: AccelerationXYZ, RotationVelocityXYZ
  int16_t ax, ay, az; // int 16 bits
  int16_t gx, gy, gz;
  accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  //accelgyro.getAcceleration(&ax, &ay, &az);
  currentSensorData.accelerationX = ax;
  currentSensorData.accelerationY = ay;
  currentSensorData.accelerationZ = az;
  currentSensorData.velocityRotationX = gx;
  currentSensorData.velocityRotationY = gy;
  currentSensorData.velocityRotationZ = gz;

  // SI1145
  currentSensorData.UVIndex = uv.readUV() / 100.0;

  // GPS
  while (gps_serial.available() > 0)
  {
    if (gps.encode(gps_serial.read()))
    {
      if (gps.location.isValid()) {
        currentSensorData.latitude = (float)gps.location.lat(); // Conversion with loss
        currentSensorData.longitude = (float)gps.location.lng();
      }
    }
  }

  return currentSensorData;
}

void setup() {
  /* Initialize Remote Transmission */
  gps_serial.begin(9600);
  Serial.begin(9600); // Initialized, but only used for debugging
  radio.begin(9600);

  /* Sensor Setup */
  // BMP280
  bmp.begin(0x76);
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                 Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                 Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                 Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                 Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
  //SI1145
  uv.begin();

  //MPU6050
  accelgyro.initialize();
  Serial.println("Helios Cansat Initialized");
}

void send_data(SensorData sensorData)
{
  String paquete;

  paquete+="Helios";
  paquete+=",";
  paquete+=String(sensorData.time);
  paquete+=",";
  paquete+=String(sensorData.pressure);
  paquete+=",";
  paquete+=String(sensorData.temperature);
  paquete+=",";   
  paquete+=String(sensorData.velocityRotationX);
  paquete+=",";
  paquete+=String(sensorData.velocityRotationY);
  paquete+=",";
  paquete+=String(sensorData.velocityRotationZ);
  paquete+=",";
  paquete+=String(sensorData.accelerationX);
  paquete+=",";
  paquete+=String(sensorData.accelerationY);
  paquete+=",";
  paquete+=String(sensorData.accelerationZ);
  paquete+=",";
  paquete+=String(sensorData.latitude);
  paquete+=",";
  paquete+=String(sensorData.longitude);
  paquete+=",";
  paquete+=String(sensorData.UVIndex);
  Serial.println(paquete);   
  radio.println(paquete);
}

void loop() { 
  //Serial.println("Attempting to fetch data");
  SensorData s_data = collectSensorData();
  //Serial.println("Data fetched, sending...");
  send_data(s_data);
  //Serial.println("Waiting 1s");
  delay(1000);
}
