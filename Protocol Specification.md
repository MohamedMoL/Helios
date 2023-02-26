# Helios Satellite Protocol Specification

**NOTE: THIS SPECIFICATION IS NOT YET FINISHED, IT'S SUBJECT TO BREAKING CHANGES IN THE NEAR FUTURE**

This is the technical specification of the transmission protocol to be used on the satellite.

There are currently two competing formats for data transmission:
- Text (Comma Separated Value)
- Binary (Helios Binary Data Packet)

# Sensors and data

The Helios Satellite is an Arduino Uno (Rev. 3) board with the following components connected via I2C or UART:

| Component Name | Arduino Pin                | Module Pin                |
|----------------|----------------------------|---------------------------|
| APC220         | [5v, GND, D8(RX), D9(TX)]  | [VCC, GND, TXD, RXD]      |
| NEO-M8N        | [5v, GND, D2(RX), D3(TX)]  | [VCC, GND, TX, RX]        |
| GY521/MPU6050  | [5v, GND, SCL, SDA]        | [VCC, GND, SCL, SDA]      |
| BMP280         | [3v3, GND, SCL, SDA]       | [VCC, GND, SCL, SDA]      |
| GY1145/SI1145  | [5v, GND, SCL, SDA]        | [VIN, GND, SCL, SDA]      |

The software onboard will collect the following data:

| Name                  | Format        | Notes                                               |
|-----------------------|---------------|-----------------------------------------------------|
| ID                    | String        | Team name, satellte identifier                      |
| Time                  | Unsigned Long | Arduino Power-on Timer, in ms                       |
| Pressure              | Float         | BMP280: Pressure, in Pascals                        |
| Temperature           | Float         | BMP280: Temperature, in ºC                          |
| AccelerationRotationX | Float         | MPU6050: Rotation in direction X, in degrees/second |
| AccelerationRotationY | Float         | MPU6050: Rotation in direction Y, in degrees/second |
| AccelerationRotationZ | Float         | MPU6050: Rotation in direction Z, in degrees/second |
| AccelerationX         | Float         | MPU6050: Acceleration on X axis, in g forces        |
| AccelerationY         | Float         | MPU6050: Acceleration on Y axis, in g forces        |
| AccelerationZ         | Float         | MPU6050: Acceleration on Z axis, in g forces        |
| Latitude              | Float         | NEO-M8N: GCS in degrees                             |
| Longitude             | Float         | NEO-M8N: GCS in degrees                             |
| UVIndex               | Float         | SI1145: UV Index                                    |

# Reed-Solomon Configuration

48 ECC Symbols per 196 characters (bytes)

Which means 148 characters are taken up by the payload, and the 48 remaining characters are for error correction.

The payload can have up to 24 erratas before it becomes unrepairable.
# Text

## Packet Payload

The plain data MUST be an **ASCII** encoded string, an entry of CSV MUST display the data entries in the following order:

`ID,Time,Altitude,Pressure,Temperature,AccelerationRotationX,AccelerationRotationY,AccelerationRotationZ,AccelerationX,AccelerationY,AccelerationZ,Latitude,Longitude,UVIndex`

## Payload Encryption

In text mode, the packets cannot be encrypted, this mode only exists for debugging purposes.

## Error Correction

Reed-Solomon error correction codes will be added to the to the end of the plain text payload

## Packet encapsulation and construction

`[Text Payload][Reed-Solomon ECC of Text Payload][CRLF]`
# Binary

Not implemented yet