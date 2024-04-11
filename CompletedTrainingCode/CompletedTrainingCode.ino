#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include "CircularBuffer.hpp"
#include <FastLED.h>

#define pin_neopixel 18

#define NUM_LEDS 5

#define pin_button1 0

#define pin_button2 47

Adafruit_MPU6050 mpu;

//threshold for detecting an impact
int impactThreshold = 350;
// Define the size of the circular buffer
const int bufferSize = 100;
//Used for increasing the adjustment interval
const byte adjust = 25;

// Define the data type to store in the buffer
struct SensorData {
  int acc;
  int x;
  int y;
  int z;
};


// Create a circular buffer object
CircularBuffer<SensorData, bufferSize> sensorBuffer;

CRGB leds[NUM_LEDS];
int MAX_READING = 750;

void setup() {
  Serial.begin(9600);
  while (!Serial)
    delay(10);  // will pause Zero, Leonardo, etc until serial console opens

  //Lighting Stuff
  FastLED.addLeds<NEOPIXEL, pin_neopixel>(leds, NUM_LEDS);
  FastLED.setBrightness(50);

  //Button Stuff
  pinMode(pin_button1, INPUT_PULLUP);
  pinMode(pin_button2, INPUT_PULLUP);

  //Accelerometer Stuff
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
  if (!digitalRead(pin_button1)) {
    int sum = 0;
    for (int i = 0; i < 8; i++) {
      sum += !digitalRead(pin_button1);
    }
    if (sum == 8 && impactThreshold < MAX_READING) {
      impactThreshold += adjust;
    }
    tuningDisplay();
  }

  if (!digitalRead(pin_button2)) {
    int sum = 0;
    for (int i = 0; i < 8; i++) {
      sum += !digitalRead(pin_button2);
    }
    if (sum == 8 && impactThreshold > 0) {
      impactThreshold -= adjust;
    }
    tuningDisplay();
  }
  /* Get new sensor events with the readings */

  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);



  int xMap = (a.acceleration.x) * 10;

  int yMap = (a.acceleration.y) * 10;

  int zMap = (a.acceleration.z + 1) * 10;

  int mag = round(sqrt(xMap * xMap + yMap * yMap + zMap * zMap));

  // Create a sensor data object to store readings
  SensorData data = { mag, xMap, yMap, zMap };
  addSensorData(data);

  // Impact detection logic (using latest data)
  if (mag > impactThreshold) {
    int i = 0;
    while (!sensorBuffer.isEmpty() && i < 50) {
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
  impactDisplay(mag);
  }
  Serial.println("");


  for (int led = 0; led < NUM_LEDS; led++) {
    leds[led] = CRGB::Black;
    FastLED.show();
  }

  delay(10);
}

// Function to add sensor data to the circular buffer (overwrites oldest)
void addSensorData(SensorData data) {
  if (sensorBuffer.isFull()) {
    // Overwrite the oldest data by popping the front element first
    sensorBuffer.pop();
  }
  sensorBuffer.push(data);
}

void tuningDisplay() {
  int mappedValue = map(impactThreshold, 0, MAX_READING, 1, 5);
  Serial.println(impactThreshold);
  ledDisplay(mappedValue);
  delay(500);
}

void impactDisplay(int magnitude){
  int mappedValue = map(magnitude, 0, MAX_READING, 1, 5);
  ledDisplay(mappedValue);
  delay(125);
}

void ledDisplay(int value){
  switch (value) {
    case 1:
      leds[0] = CRGB::Red;
      FastLED.show();
      break;
    case 2:
      leds[0] = CRGB::Red;
      leds[1] = CRGB::Yellow;
      FastLED.show();
      break;
    case 3:
      leds[0] = CRGB::Red;
      leds[1] = CRGB::Yellow;
      leds[2] = CRGB::Green;
      FastLED.show();
      break;
    case 4:
      leds[0] = CRGB::Red;
      leds[1] = CRGB::Yellow;
      leds[2] = CRGB::Green;
      leds[3] = CRGB::Yellow;
      FastLED.show();
      break;
    case 5:
      leds[0] = CRGB::Red;
      leds[1] = CRGB::Yellow;
      leds[2] = CRGB::Green;
      leds[3] = CRGB::Yellow;
      leds[4] = CRGB::Red;
      FastLED.show();
      break;
  }
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