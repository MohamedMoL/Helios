#include <limits.h>
struct SensorData {
  /* Onboard timer */
  long time = 0; // ms
  /* BMP280 (Pressure, temperature) */ 
  float temperature = 0; // degrees celsius
  float pressure = 0; // pascals
  // MPU6050 (Gyroscope / Accelerometer)
  float velocityRotationX = 0; // degrees per second
  float velocityRotationY = 0; // degrees per second
  float velocityRotationZ = 0; // degrees per second
  float accelerationX = 0; // meters per second squared (m^s2)
  float accelerationY = 0; // meters per second squared (m^s2)
  float accelerationZ = 0; // meters per second squared (m^s2)
  // NEO-M8N (GPS)
  float latitude = NAN;
  float longitude = NAN;
  // SI1145 (UV Index)
  float UVIndex = 0;
};
