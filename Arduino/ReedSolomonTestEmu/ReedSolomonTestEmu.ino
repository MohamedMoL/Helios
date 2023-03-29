#include <limits.h>
#include "RS-FEC.h"

RS::ReedSolomon<60, 48> rs;

float latitude = NAN;
float longitude = NAN;
unsigned long timer = millis();

struct SensorData {
    unsigned long time = ULONG_MAX;
    float pressure = NAN;
    float temperature = NAN;
    float velocityRotationX = NAN;
    float velocityRotationY = NAN;
    float velocityRotationZ = NAN;
    float accelerationX = NAN;
    float accelerationY = NAN;
    float accelerationZ = NAN;
    float angleX = NAN;
    float angleY = NAN;
    float angleZ = NAN;
    float latitude = NAN;
    float longitude = NAN;
    float uvIndex = NAN;
};

void setup()
{
    Serial.begin(9600);
}

SensorData CollectSensorData(unsigned long currentTime, float latitude, float longitude) {
    // currentTime, Longitude and Latitude depend on external variables
    SensorData currentSensorData;

    currentSensorData.time = currentTime; // Arduino: Power-on timer
    currentSensorData.pressure = 0; // BMP280: Pressure
    currentSensorData.temperature = 0; // BMP280: Temperature
    currentSensorData.velocityRotationX = 0; // MPU6050: Angular Velocity X
    currentSensorData.velocityRotationY = 0; // MPU6050: Angular Velocity Y
    currentSensorData.velocityRotationZ = 0; // MPU6050: Angular Velocity Z
    currentSensorData.accelerationX = 0; // MPU6050: Acceleration X Axis
    currentSensorData.accelerationY = 0; // MPU6050: Acceleration Y Axis
    currentSensorData.accelerationZ = 0; // MPU6050: Acceleration Z Axis
    currentSensorData.angleX = 0; // MPU6050: Angle X (Pitch)
    currentSensorData.angleY = 0; // MPU6050: Angle Y (Roll)
    currentSensorData.angleZ = 0; // MPU6050: Angle Z (Yaw)
    currentSensorData.latitude = latitude;
    currentSensorData.longitude = longitude;
    currentSensorData.uvIndex = 0;

    return currentSensorData;
}

void SendPacket(SensorData &s)
{
    // Data Transmission, Binary, ECC

    // ASCII Header
    Serial.print("Helios");
    
    // Payload is already provided by SensorData &s parameter
    
    uint8_t* payloadPtr = reinterpret_cast<uint8_t*>(&s);
    Serial.write(payloadPtr, sizeof(s));
}

void loop()
{    
    // Timer
    unsigned long currentTime = millis();
    
    // GPS Coordinates
    latitude = -20;
    longitude = -155;
    
    if (currentTime - timer > 1000)
    {
        SensorData currentSensorDataCollection = CollectSensorData(currentTime, latitude, longitude);
        SendPacket(currentSensorDataCollection);
        timer = currentTime;
    }
}