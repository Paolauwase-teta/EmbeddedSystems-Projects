#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  mpu.initialize();
}

void loop() {
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);
  float pitch = atan2(ax, sqrt(ay * ay + az * az)) * 180 / PI;
  float roll  = atan2(ay, sqrt(ax * ax + az * az)) * 180 / PI;
  Serial.print(pitch);
  Serial.print(",");
  Serial.println(roll);
  delay(50);
}
