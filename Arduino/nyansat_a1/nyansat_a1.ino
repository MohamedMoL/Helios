#define CANSAT_NAME "Helios"

#include <Adafruit_BMP280.h>
#include <Adafruit_SI1145.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <TinyGPS++.h>
#include <AltSoftSerial.h>
#include <limits.h>

// Note: GPS RX/TX will be connected to HardwareSerial. RX0 TX1
TinyGPSPlus gps;
Adafruit_BMP280 bmp;
Adafruit_SI1145 uv = Adafruit_SI1145();
AltSoftSerial radio;
Adafruit_MPU6050 accelgyro;

void setup()
{
    Serial.begin(9600); // GPS
    radio.begin(9600); // Radio
    bmp.begin(0x76); // BMP280 Pressure and temperature sensor
    bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
    uv.begin(); // SI1145 UV Light sensor
    accelgyro.begin(); // MPU6050 Accelerometer and Gyroscope
    accelgyro.setAccelerometerRange(MPU6050_RANGE_8_G);
    accelgyro.setGyroRange(MPU6050_RANGE_500_DEG);
    accelgyro.setFilterBandwidth(MPU6050_BAND_21_HZ);
}

void loop()
{
    // Data collection phase
    long time = millis(); // Timer
    float pressure = bmp.readPressure(); // BMP280: Pressure
    float temperature = bmp.readTemperature(); // BMP280: Temperature
    // MPU6050: Angular velocity and acceleration on 3 axis
    sensors_event_t a, g, temp;
    accelgyro.getEvent(&a, &g, &temp);
    float velocityRotationX = g.gyro.x; // m/s^2
    float velocityRotationY = g.gyro.y;
    float velocityRotationZ = g.gyro.z;
    float accelerationX = a.acceleration.x; // rad/s
    float accelerationY = a.acceleration.y;
    float accelerationZ = a.acceleration.z;
    float UVIndex = uv.readUV() / 100.0; // SI1145: UV Index
    // GPS Coordinates, let's hope that this time this shit will work
    float latitude = -999.9;
    float longitude = -999.9;
    while (Serial.available() > 0)
    {
        if (gps.encode(Serial.read()))
        {
            if (gps.location.isValid()) {
                latitude = (float)gps.location.lat(); // Conversion with loss
                longitude = (float)gps.location.lng();
            } else {
                latitude = NAN;
                longitude = NAN;
            }
        }
    }

    radio.print("Helios,");
    radio.print(time); radio.print(",");
    radio.print(pressure); radio.print(",");
    radio.print(temperature); radio.print(",");
    radio.print(velocityRotationX); radio.print(",");
    radio.print(velocityRotationY); radio.print(",");
    radio.print(velocityRotationZ); radio.print(",");
    radio.print(accelerationX); radio.print(",");
    radio.print(accelerationY); radio.print(",");
    radio.print(accelerationZ); radio.print(",");
    radio.print(latitude); radio.print(",");
    radio.print(longitude); radio.print(",");
    radio.println(UVIndex);
    delay(1000); // This is causing TinyGPS fail to fetch data
}