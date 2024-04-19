#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <String.h>

BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
bool deviceConnected = false;
bool oldDeviceConnected = false;
uint32_t value = 0;
String output_string;

#define SERVICE_UUID "4fafc201-1fb5-459e-8fcc-c5c9c331914b"         //The name of the device
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"  //Package


class MyServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer* pServer) {
    deviceConnected = true;
  };

  void onDisconnect(BLEServer* pServer) {
    deviceConnected = false;
  }
};


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
  int label;
  int thresh;
  int acc;
  int x;
  int y;
  int z;
  int xr;
  int yr;
  int zr;
};


// Create a circular buffer object
CircularBuffer<SensorData, bufferSize> sensorBuffer;

CRGB leds[NUM_LEDS];
int MAX_READING = 750;
int thresh = 0;

void setup() {
  Serial.begin(115200);

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
  // Serial.print("Booting...");
  delay(100);

  // Create the BLE Device
  BLEDevice::init("Hambone-V1");

  // Create the BLE Server
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  // Create the BLE Service
  BLEService* pService = pServer->createService(SERVICE_UUID);

  // Create a BLE Characteristic
  pCharacteristic = pService->createCharacteristic(
    CHARACTERISTIC_UUID,
    BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_WRITE | BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_INDICATE);

  // https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.descriptor.gatt.client_characteristic_configuration.xml
  // Create a BLE Descriptor
  pCharacteristic->addDescriptor(new BLE2902());

  // Start the service
  pService->start();

  // Start advertising
  BLEAdvertising* pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(false);
  pAdvertising->setMinPreferred(0x0);  // set value to 0x00 to not advertise this parameter
  BLEDevice::startAdvertising();
  Serial.println("Waiting a client connection to notify...");
}

void loop() {

  // notify changed value
  if (deviceConnected) {
    Serial.println("...");
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

    int xrMap = (g.gyro.x) * 10;

    int yrMap = (g.gyro.y) * 10;

    int zrMap = (g.gyro.z) * 10;

    int mag = round(sqrt(xMap * xMap + yMap * yMap + zMap * zMap));

    SensorData data = { thresh, mag, xMap, yMap, zMap, xrMap, yrMap, zrMap };
    addSensorData(data);

    // Impact detection logic (using latest data)
    if (mag > impactThreshold) {
      thresh = 1;
      impactDisplay(mag);
    } else {
      thresh = 0;
    }

    // Serial.println("0, " + String(thresh) + ", " + String(mag) + ", " + String(xMap) + ", " + String(yMap) + ", " + String(zMap) + ", " + String(xrMap) + ", " + String(yrMap) + ", " + String(zrMap));

    if (mag > impactThreshold) {
      int i = 0;
      while (!sensorBuffer.isEmpty() && i < 60) {
        SensorData latestData = sensorBuffer.pop();
        output_string = String(latestData.acc) + ", " + String(latestData.x) + ", " + String(latestData.y) + ", " + String(latestData.z) + ", " + String(latestData.xr) + ", " + String(latestData.yr) + ", " + String(latestData.zr);
        i++;
        std::string stdString = output_string.c_str();
        pCharacteristic->setValue(stdString);
        pCharacteristic->notify();
      }
      impactDisplay(mag);
    }
    Serial.println("");
    for (int led = 0; led < NUM_LEDS; led++) {
      leds[led] = CRGB::Black;
      FastLED.show();
    }

    delay(10);  // bluetooth stack will go into congestion, if too many packets are sent, in 6 hours test i was able to go as low as 3ms
  }
  // disconnecting
  if (!deviceConnected && oldDeviceConnected) {
    delay(500);                   // give the bluetooth stack the chance to get things ready
    pServer->startAdvertising();  // restart advertising
    oldDeviceConnected = deviceConnected;
  }
  // connecting
  if (deviceConnected && !oldDeviceConnected) {
    // do stuff here on connecting
    oldDeviceConnected = deviceConnected;
  }
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

void impactDisplay(int magnitude) {
  int mappedValue = 0;

  if (magnitude > MAX_READING) {
    mappedValue = 5;
  } else {
    mappedValue = map(magnitude, 0, MAX_READING, 1, 5);
  }
  ledDisplay(mappedValue);
  delay(125);
}

void ledDisplay(int value) {
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
