#include <TinyGPSPlus.h>
#include <SoftwareSerial.h>

TinyGPSPlus gps;
SoftwareSerial gps_serial(2, 3);

void setup()
{
  Serial.begin(9600);
  gps_serial.begin(9600);
  Serial.println(F("gps_code_test.ino"));
  Serial.println();
}

void loop()
{
  // This sketch displays information every time a new sentence is correctly encoded.
  while (gps_serial.available() > 0)
    if (gps.encode(gps_serial.read()))
    {
        Serial.print(F("Location: ")); 
        if (gps.location.isValid())
        {
          Serial.print(gps.location.lat(), 6);
          Serial.print(F(","));
          Serial.print(gps.location.lng(), 6);
        }
        else
        {
          Serial.print(F("INVALID"));
        }
      
        Serial.println();
    }
}
