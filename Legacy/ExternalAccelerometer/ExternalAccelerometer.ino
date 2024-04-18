// Basic demo for accelerometer readings from Adafruit MPU6050

// ESP32 Guide: https://RandomNerdTutorials.com/esp32-mpu-6050-accelerometer-gyroscope-arduino/
// ESP8266 Guide: https://RandomNerdTutorials.com/esp8266-nodemcu-mpu-6050-accelerometer-gyroscope-arduino/
// Arduino Guide: https://RandomNerdTutorials.com/arduino-mpu-6050-accelerometer-gyroscope/

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include "CircularBuffer.hpp"

Adafruit_MPU6050 mpu;

//threshold for detecting an impact
int impactThreshold = 350;
// Define the size of the circular buffer
const int bufferSize = 100;

// Define the data type to store in the buffer
struct SensorData {
  int acc;
  int x;
  int y;
  int z;
};


// Create a circular buffer object
CircularBuffer<SensorData, bufferSize> sensorBuffer;

void setup(void) {
  Serial.begin(9600);
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Adafruit MPU6050 test!");

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  delay(100);
}

void loop() {
  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);



  int xMap = (a.acceleration.x) * 10;

  int yMap = (a.acceleration.y) * 10;

  int zMap = (a.acceleration.z+1) * 10;

  int mag = round(sqrt(xMap * xMap + yMap * yMap + zMap * zMap));

  // Create a sensor data object to store readings
  SensorData data = {mag, xMap, yMap, zMap };
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
  Serial.println("");
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