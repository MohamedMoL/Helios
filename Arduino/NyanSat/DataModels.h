struct SensorData {
  /* Onboard timer */
  long time; // ms
  /* BMP280 (Pressure, temperature) */ 
  float temperature; // degrees celsius
  float pressure; // pascals
  // MPU6050 (Gyroscope / Accelerometer)
  float velocityRotationX; // degrees per second
  float velocityRotationY; // degrees per second
  float velocityRotationZ; // degrees per second
  float accelerationX; // meters per second squared (m^s2)
  float accelerationY; // meters per second squared (m^s2)
  float accelerationZ; // meters per second squared (m^s2)
  // NEO-M8N (GPS)
  float latitude;
  float longitude;
  // SI1145 (UV Index)
  float UVIndex;
};
