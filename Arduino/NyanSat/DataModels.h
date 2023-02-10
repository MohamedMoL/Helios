struct SensorData {
  // Onboard timer
  long time;
  // BMP280 (Pressure, temperature)
  float temperature;
  float pressure;
  // SI1145 (Visible Light, Infrared light, UV Index)
  int visibleLight;
  int infraredLight;
  float UVIndex;
};
