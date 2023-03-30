#include <Adafruit_BMP280.h>
#include <Adafruit_SI1145.h>
#include <MPU6050_light.h>
#include <Adafruit_Sensor.h>
#include <TinyGPS++.h>
#include <AltSoftSerial.h>
#include <limits.h>
#include "DataModel.h"

// Note: GPS RX/TX will be connected to HardwareSerial. RX0 TX1
TinyGPSPlus gps;
Adafruit_BMP280 bmp;
Adafruit_SI1145 uv = Adafruit_SI1145();
AltSoftSerial radio;
MPU6050 mpu(Wire);

double latitude = NAN;
double longitude = NAN;
unsigned long timer = millis();

void setup()
{
    Wire.begin();
    Serial.begin(9600); // GPS
    radio.begin(9600); // Radio
    bmp.begin(0x76); // BMP280 Pressure and temperature sensor
    bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
    uv.begin(); // SI1145 UV Light sensor
    mpu.begin(); // MPU6050 Gyro and accelerometer
    mpu.setAccConfig(0);
    mpu.setGyroConfig(0);
    mpu.calcOffsets(true,true);
}

SensorData CollectSensorData(unsigned long currentTime, double latitude, double longitude) {
    // currentTime, Longitude and Latitude depend on external variables
    SensorData currentSensorData;

    currentSensorData.time = currentTime; // Arduino: Power-on timer
    currentSensorData.pressure = bmp.readPressure(); // BMP280: Pressure
    currentSensorData.temperature = bmp.readTemperature(); // BMP280: Temperature
    currentSensorData.altitude = bmp.readAltitude(); // Altitude derived from pressure, seaLevelHPA = 1013.25
    currentSensorData.velocityRotationX = mpu.getGyroX(); // MPU6050: Angular Velocity X
    currentSensorData.velocityRotationY = mpu.getGyroY(); // MPU6050: Angular Velocity Y
    currentSensorData.velocityRotationZ = mpu.getGyroZ(); // MPU6050: Angular Velocity Z
    currentSensorData.accelerationX = mpu.getAccX(); // MPU6050: Acceleration X Axis
    currentSensorData.accelerationY = mpu.getAccY(); // MPU6050: Acceleration Y Axis
    currentSensorData.accelerationZ = mpu.getAccZ(); // MPU6050: Acceleration Z Axis
    currentSensorData.angleX = mpu.getAngleX(); // MPU6050: Angle X (Pitch)
    currentSensorData.angleY = mpu.getAngleY(); // MPU6050: Angle Y (Roll)
    currentSensorData.angleZ = mpu.getAngleZ(); // MPU6050: Angle Z (Yaw)
    currentSensorData.latitude = latitude;
    currentSensorData.longitude = longitude;
    currentSensorData.uvIndex = uv.readUV() / 100.0;

    return currentSensorData;
}

void SendPacket(SensorData s)
{
    // Data Transmission, No ECC
    radio.print("Helios,");
    radio.print(s.time); radio.print(",");
    radio.print(s.pressure); radio.print(",");
    radio.print(s.temperature); radio.print(",");
    radio.print(s.altitude); radio.print(",");
    radio.print(s.velocityRotationX); radio.print(",");
    radio.print(s.velocityRotationY); radio.print(",");
    radio.print(s.velocityRotationZ); radio.print(",");
    radio.print(s.accelerationX); radio.print(",");
    radio.print(s.accelerationY); radio.print(",");
    radio.print(s.accelerationZ); radio.print(",");
    radio.print(s.angleX); radio.print(",");
    radio.print(s.angleY); radio.print(",");
    radio.print(s.angleZ); radio.print(",");
    radio.print(s.latitude, 9); radio.print(",");
    radio.print(s.longitude, 9); radio.print(",");
    radio.println(s.uvIndex);
}

void loop()
{    
    // Timer
    unsigned long currentTime = millis();

    // MPU6050
    mpu.update();
    
    // GPS Coordinates
    while (Serial.available() > 0)
    {
        if (gps.encode(Serial.read()))
        {
            if (gps.location.isValid()) {
                latitude = gps.location.lat();
                longitude = gps.location.lng();
            }
        }
    }
    
    if (currentTime - timer > 1000)
    {
        SensorData currentSensorDataCollection = CollectSensorData(currentTime, latitude, longitude);
        SendPacket(currentSensorDataCollection);
        timer = currentTime;
    }
}