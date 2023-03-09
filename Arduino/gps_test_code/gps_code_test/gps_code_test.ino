#include <SoftwareSerial.h>
#include <TinyGPS++.h>
#include <AltSoftSerial.h>

SoftwareSerial gps_serial(2, 3);
AltSoftSerial radio;

TinyGPSPlus gps;

void setup()
{
    Serial.begin(9600);
    gps_serial.begin(9600);
}

void loop() { 
  while (gps_serial.available() > 0)
  {
    char r = gps_serial.read();
    gps.encode(r);
    Serial.print(r);
  }

  if (gps.location.isValid()) {
    float lat = (float)gps.location.lat();
    float lng = (float)gps.location.lng();
    Serial.println(lat);
    Serial.println(lng);
    radio.println(lat);
    radio.println(lng);
  } else {
    Serial.println("Invalid GPS data");
    radio.println("Invalid GPS data");
  }
  
  //Serial.println("Waiting 1s");
  delay(1000);
}
