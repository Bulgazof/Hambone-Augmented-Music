#include <Wire.h>
#include "SparkFun_BMI270_Arduino_Library.h"
#include "CircularBuffer.hpp"
#include <vector>

#define pin_i2c_sda 8
#define pin_i2c_scl 9

// Define the data type to store in the buffer
struct SensorData {
  int acc;
  int x;
  int y;
  int z;
};

// Define the size of the circular buffer
const int bufferSize = 100;

// Create a circular buffer object
CircularBuffer<SensorData, bufferSize> sensorBuffer;

// Create a new sensor object
BMI270 imu;

// I2C address selection
uint8_t i2cAddress = BMI2_I2C_SEC_ADDR;  // 0x69

// impact calibration
byte impactThreshold = 20;

void setup() {
  // Start serial
  Serial.begin(9600);
  // Initialize the I2C library
  Wire.begin();

  // Check if sensor is connected and initialize
  // Address is optional (defaults to 0x68)
  while (imu.beginI2C(i2cAddress) != BMI2_OK) {
    // Not connected, inform user
    Serial.println("Error: BMI270 not connected, check wiring and I2C address!");
    // Wait a bit to see if connection is established
    delay(1000);
  }

  Serial.println("BMI270 connected!");
}

void loop() {
  // Get measurements from the sensor
  imu.getSensorData();

  int xMap = imu.data.accelX * 50;

  int yMap = imu.data.accelY * 50;

  int zMap = imu.data.accelZ * 50;

  int mag = round(sqrt(imu.data.accelX * imu.data.accelX + imu.data.accelY * imu.data.accelY + imu.data.accelZ * imu.data.accelZ) * 1000) / 100;

  // Create a sensor data object to store readings
  SensorData data = {mag, xMap, yMap, zMap };

  // Add sensor data to the circular buffer
  addSensorData(data);

  // Impact detection logic (using latest data)
  if (mag > impactThreshold) {
    int i = 0;
    while (!sensorBuffer.isEmpty() && i<50) {
      SensorData latestData = sensorBuffer.pop();
      Serial.print(latestData.acc);
      Serial.print(", ");
      Serial.print(latestData.x);
      Serial.print(", ");
      Serial.print(latestData.y);
      Serial.print(", ");
      Serial.println(latestData.z);
      i++;
    }
  }
  else{
  Serial.print(0);
  Serial.print(", ");
  Serial.print(0);
  Serial.print(", ");
  Serial.print(0);
  Serial.print(", ");
  Serial.println(0);
  }

  // Serial.println("");
  delay(20);
}

// Function to add sensor data to the circular buffer (overwrites oldest)
void addSensorData(SensorData data) {
  if (sensorBuffer.isFull()) {
    // Overwrite the oldest data by popping the front element first
    sensorBuffer.pop();
  }
  sensorBuffer.push(data);
}

// Function to get the latest sensor data from the buffer (returns a copy)
SensorData getLatestData() {
  if (!sensorBuffer.isEmpty()) {
    return sensorBuffer.last();
  } else {
    // Handle empty buffer condition (e.g., return default values or error)
    Serial.println("Buffer empty!");
    SensorData emptyData = { 0, 0, 0 };
    return emptyData;
  }
}

