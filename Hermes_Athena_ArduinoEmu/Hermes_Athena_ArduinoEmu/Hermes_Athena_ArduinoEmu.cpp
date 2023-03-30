#include <iostream>
#include <chrono>
#include <serial/serial.h>
#include <windows.h>
#include <stdio.h>
#include <limits.h>
#include <string>
#include <cstdint>
#include "RS-FEC.h"
#include "ArduinoQueue.h"

using namespace std;
using namespace serial;

void loop(); // Arduino loop function declared
void setup(); // Arduino setup function declared
Serial Serial1("COM5", 9600); // Arduino Serial, CHANGEME

class c_radio {
public:
    static void write(uint8_t* data, size_t length)
    {
        Serial1.write(data, length);
    }
    static void print(float a)
    {
        Serial1.write(to_string(a));
    }
    static void print(const string &data)
    {
        Serial1.write(data);
    }
    static void print(unsigned long a)
    {
        Serial1.write(to_string(a));
    }
    static void print(double a)
    {
        Serial1.write(to_string(a));
    }
    static void println(float a)
    {
        Serial1.write(to_string(a));
        Serial1.write("\r\n");
    }
};

// Windows event handler, or _interrupts_ if you want to be fancy
// Checks if CTRL+C is pressed, and if it is, quit the program and release all file handles
bool running;
BOOL WINAPI consoleHandler(DWORD signal) {

    if (signal == CTRL_C_EVENT)
    {
        printf("Ctrl-C handled\n"); // do cleanup
        running = FALSE;
        printf("Releasing Serial handle...\n");
        Serial1.flush();
        Serial1.close();
    }

    return TRUE;
}

auto startTime = chrono::high_resolution_clock::now();

unsigned long millis()
{
    auto currentTick = chrono::high_resolution_clock::now();
    chrono::duration<double> deltaStartTime = currentTick - startTime;
    chrono::milliseconds deltaStartTimeMs = chrono::duration_cast<chrono::milliseconds>(deltaStartTime);
    long current_ms = deltaStartTimeMs.count();
    return current_ms;
}

int randint(int min, int max)
{
    // Generates a number in [min, max) range
    int random = min + (rand() % max);
    return random;
}

float randfloat(int LO, int HI)
{
    // Generates a random floating point number between [LO, HI]    
    float r3 = LO + static_cast <float> (rand()) / (static_cast <float> (RAND_MAX / (HI - LO)));
    return r3;
}

int main()
{
	// https://stackoverflow.com/questions/18291284/handle-ctrlc-on-win32
    running = TRUE;
    if (!SetConsoleCtrlHandler(consoleHandler, TRUE)) {
        printf("\nERROR: Could not set control handler");
        return 1;
    }

    srand(0);
    setup();

    while (running)
        loop();

    printf("Quitting program\n");
    return 0;
}

// This project emulates the actual C++ structure of the NyanSat
// It also allows me to analyze and learn how C++ actually behaves (Stuff like memory management)

/* GLOBAL SPACE */

#pragma pack(1) // Remove padding at bottom
struct SensorData{
    uint32_t time = MAXUINT32;
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
    float uvIndex = NAN; // 4 bytes of padding here, should be removed to match protocol specification
};

float latitude = NAN;
float longitude = NAN;
unsigned long timer = millis();
RS::ReedSolomon<60, 48> rs;
//ArduinoQueue<SensorData> queue(8);

SensorData CollectSensorData(unsigned long currentTime, double latitude, double longitude) {
    // currentTime, Longitude and Latitude depend on external variables
    SensorData currentSensorData;

    currentSensorData.time = currentTime; // Arduino: Power-on timer
    currentSensorData.pressure = randfloat(100900, 101000); // BMP280: Pressure
    currentSensorData.temperature = randfloat(-20, 85); // BMP280: Temperature
    currentSensorData.velocityRotationX = randfloat(0, 500); // MPU6050: Angular Velocity X
    currentSensorData.velocityRotationY = randfloat(0, 500); // MPU6050: Angular Velocity Y
    currentSensorData.velocityRotationZ = randfloat(0, 500); // MPU6050: Angular Velocity Z
    currentSensorData.accelerationX = randfloat(0, 4); // MPU6050: Acceleration X Axis
    currentSensorData.accelerationY = randfloat(0, 4); // MPU6050: Acceleration Y Axis
    currentSensorData.accelerationZ = randfloat(0, 4); // MPU6050: Acceleration Z Axis
    currentSensorData.angleX = randfloat(-360, 360); // MPU6050: Angle X (Pitch)
    currentSensorData.angleY = randfloat(-360, 360); // MPU6050: Angle Y (Roll)
    currentSensorData.angleZ = randfloat(-360, 360); // MPU6050: Angle Z (Yaw)
    currentSensorData.latitude = latitude;
    currentSensorData.longitude = longitude;
    currentSensorData.uvIndex = randfloat(0, 14);

    return currentSensorData;
}

void SendPacket(SensorData &s)
{
    c_radio radio;
    // Data Transmission, with ECC
    
    // ASCII Header
    radio.print("Helios");
    
    // Payload is already provided by SensorData &s parameter
    
    // ECC
    char payloadWithECC[60 + 48];
    rs.Encode(&s, payloadWithECC);
    radio.write((uint8_t*)payloadWithECC, 108);

    cout << "Sent " << sizeof(payloadWithECC) << " bytes" << endl;
}

/* SETUP */
void setup()
{
    // CanSat initialization code
    // Do nothing here
    return;
}

/* LOOP */
void loop()
{
    unsigned long currentTime = millis();
    latitude = randfloat(-90, 90);
    longitude = randfloat(-180, 180);

    if (currentTime - timer > 1000)
    {
        SensorData currentSensorDataCollection = CollectSensorData(currentTime, latitude, longitude);
        SendPacket(currentSensorDataCollection);
        timer = currentTime;
    }
}