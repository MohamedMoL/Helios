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
| VelocityRotationX     | Float         | MPU6050: Rotation in direction X, in degrees/second |
| VelocityRotationY     | Float         | MPU6050: Rotation in direction Y, in degrees/second |
| VelocityRotationZ     | Float         | MPU6050: Rotation in direction Z, in degrees/second |
| AccelerationX         | Float         | MPU6050: Acceleration on X axis, in g forces        |
| AccelerationY         | Float         | MPU6050: Acceleration on Y axis, in g forces        |
| AccelerationZ         | Float         | MPU6050: Acceleration on Z axis, in g forces        |
| AngleX                | Float         | MPU6050: Angle on X axis (Pitch), in degrees        |
| AngleY                | Float         | MPU6050: Angle on Y axis (Roll), in degrees         |
| AngleZ                | Float         | MPU6050: Angle on Z axis (Yaw), in degrees          |
| Latitude              | Double        | NEO-M8N: GCS in degrees                             |
| Longitude             | Double        | NEO-M8N: GCS in degrees                             |
| UVIndex               | Float         | SI1145: UV Index                                    |

# Reed-Solomon Configuration

48 ECC Symbols per 116 characters (bytes)

This means that 68 characters/bytes are taken up by the payload, and the remaining 48 characters/bytes are for error correction.

The payload can have up to 24 erratas before it becomes unrepairable.

*1 Byte = 1 Character
# Text

## Packet Payload

The plain data MUST be an **ASCII** encoded string, an entry of CSV MUST display the data entries in the following order:

`ID,Time,Pressure,Temperature,VelocityRotationX,VelocityRotationY,VelocityRotationZ,AccelerationX,AccelerationY,AccelerationZ,AngleX,AngleY,AngleZ,Latitude,Longitude,UVIndex`

Field `ID` will always be `Helios`

## Error Correction

Reed-Solomon error correction codes will be added to the to the end of the plain text payload

## Packet encapsulation and construction

`[Text Payload][Reed-Solomon ECC of Text Payload][CRLF]`
# Binary

Group Name in ASCII (Header) + Payload [+ ECC]

## Group Name (Header)

The group name is an arbitrary name, it must be in ASCII alphabet, lowercase or uppercase characters.
The header will be used for tracking and synchronizing packet reception. (Default: "Helios")

## Payload

The payload consists of the following data, in order:

| Order | Name                  | Format (C)    | Size    |
|-------|-----------------------|---------------|---------|
|   1   | Time                  | Unsigned Long | 4 Bytes | 4
|   2   | Pressure              | Float         | 4 Bytes | 8
|   3   | Temperature           | Float         | 4 Bytes | 12
|   4   | VelocityRotationX     | Float         | 4 Bytes | 16
|   5   | VelocityRotationY     | Float         | 4 Bytes | 20
|   6   | VelocityRotationZ     | Float         | 4 Bytes | 24
|   7   | AccelerationX         | Float         | 4 Bytes | 28
|   8   | AccelerationY         | Float         | 4 Bytes | 32
|   9   | AccelerationZ         | Float         | 4 Bytes | 36
|   10  | AngleX                | Float         | 4 Bytes | 40
|   11  | AngleY                | Float         | 4 Bytes | 44
|   12  | AngleZ                | Float         | 4 Bytes | 48
|   13  | Latitude              | Double        | 8 Bytes | 56
|   14  | Longitude             | Double        | 8 Bytes | 64
|   15  | UVIndex               | Float         | 4 Bytes | 68

The payload MUST have a size of 68 bytes.

## Error correction

ECC Codes will be added at the final, using the same configuration mentioned above.

ECC Symbols does NOT include correction code for header name, only the payload.

ECC Codes must have a size of 48 Bytes.