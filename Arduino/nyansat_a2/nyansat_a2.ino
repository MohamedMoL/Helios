#include <Adafruit_BMP280.h>
#include <Adafruit_SI1145.h>
#include <MPU6050_light.h>
#include <Adafruit_Sensor.h>
#include <TinyGPS++.h>
#include <AltSoftSerial.h>
#include <limits.h>

// Note: GPS RX/TX will be connected to HardwareSerial. RX0 TX1
TinyGPSPlus gps;
Adafruit_BMP280 bmp;
Adafruit_SI1145 uv = Adafruit_SI1145();
AltSoftSerial radio;
MPU6050 mpu(Wire);

double latitude = NAN;
double longitude = NAN;
long timer = millis();

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
    mpu.begin();
    mpu.setAccConfig(0);
    mpu.setGyroConfig(0);
    mpu.calcOffsets(true,true); // gyro and accelero
}

void loop()
{    
    
    // Timer
    long currentTime = millis();
    
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
        // BMP280: Pressure, Temperature
        float pressure = bmp.readPressure();
        float temperature = bmp.readTemperature(); // BMP280: Temperature7

        // MPU6050: Angular velocity, acceleration, angle on 3 axis
        float velocityRotationX = mpu.getGyroX();
        float velocityRotationY = mpu.getGyroY();
        float velocityRotationZ = mpu.getGyroZ();
        float accelerationX = mpu.getAccX();
        float accelerationY = mpu.getAccY();
        float accelerationZ = mpu.getAccZ();
        float angleX = mpu.getAngleX();
        float angleY = mpu.getAngleY();
        float angleZ = mpu.getAngleZ();
        
        // SI1145: UV Index
        float UVIndex = uv.readUV() / 100.0;

        // Data Transmission
        radio.print("Helios,");
        radio.print(currentTime); radio.print(",");
        radio.print(pressure); radio.print(",");
        radio.print(temperature); radio.print(",");
        radio.print(velocityRotationX); radio.print(",");
        radio.print(velocityRotationY); radio.print(",");
        radio.print(velocityRotationZ); radio.print(",");
        radio.print(accelerationX); radio.print(",");
        radio.print(accelerationY); radio.print(",");
        radio.print(accelerationZ); radio.print(",");
        radio.print(angleX); radio.print(",");
        radio.print(angleY); radio.print(",");
        radio.print(angleZ); radio.print(",");
        radio.print(latitude, 9); radio.print(",");
        radio.print(longitude, 9); radio.print(",");
        radio.println(UVIndex);
        timer = currentTime;
    }
}