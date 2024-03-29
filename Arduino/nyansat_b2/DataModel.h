#include <limits.h>

struct SensorData {
    unsigned long time = ULONG_MAX;
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
    float uvIndex = NAN;
};