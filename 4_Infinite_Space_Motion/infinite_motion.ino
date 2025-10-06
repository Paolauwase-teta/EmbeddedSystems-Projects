#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  mpu.initialize();
}

void loop() {
  int16_t gx, gy, gz;
  mpu.getRotation(&gx, &gy, &gz);
  float pitch = gx / 131.0;
  float roll  = gy / 131.0;
  float yaw   = gz / 131.0;
  Serial.print(pitch); Serial.print(",");
  Serial.print(roll);  Serial.print(",");
  Serial.println(yaw);
  delay(50);
}
