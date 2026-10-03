/*
 * =========================================================================
 * GreenPulse IoT Plant Monitoring Node — ESP32 Firmware
 * =========================================================================
 * When you receive your physical IoT hardware, follow these 3 steps:
 * 1. Connect DHT11/DHT22 Temperature & Humidity sensor to GPIO 4.
 * 2. Connect Soil Moisture sensor analog pin to GPIO 34 (ADC1).
 * 3. Enter your WiFi credentials below, and upload via Arduino IDE!
 * =========================================================================
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>   // Install ArduinoJson library in Arduino IDE
#include "DHT.h"           // Install DHT sensor library by Adafruit

// -------------------------------------------------------------
// 1. WiFi & Device Settings (Change these when hardware arrives)
// -------------------------------------------------------------
const char* WIFI_SSID     = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

const char* DEVICE_ID     = "greenpulse-001";

// -------------------------------------------------------------
// 2. Hardware Pin Definitions
// -------------------------------------------------------------
#define DHTPIN 4           // Digital pin connected to DHT sensor
#define DHTTYPE DHT22      // DHT 11 or DHT 22 (AM2302)

#define SOIL_PIN 34        // Analog pin connected to soil moisture sensor
#define AIR_VALUE 3500     // Calibration value in dry air (raw ADC)
#define WATER_VALUE 1500   // Calibration value in pure water (raw ADC)

DHT dht(DHTPIN, DHTTYPE);

// -------------------------------------------------------------
// 3. AWS Endpoint Configuration
// (Can be an AWS API Gateway HTTP URL or AWS IoT Core MQTT Endpoint)
// -------------------------------------------------------------
const char* AWS_API_ENDPOINT = "https://your-api-id.execute-api.us-east-1.amazonaws.com/reading";

void connectWiFi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected! IP: ");
  Serial.println(WiFi.localIP());
}

float readSoilMoisture() {
  int rawValue = analogRead(SOIL_PIN);
  // Map raw analog reading to percentage (0% to 100%)
  int percentage = map(rawValue, AIR_VALUE, WATER_VALUE, 0, 100);
  if (percentage < 0) percentage = 0;
  if (percentage > 100) percentage = 100;
  return (float)percentage;
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("Starting GreenPulse IoT Node...");

  dht.begin();
  connectWiFi();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  // 1. Read Physical Sensors
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  float soilMoisture = readSoilMoisture();

  // Check if read failed
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    delay(2000);
    return;
  }

  Serial.println("----------------------------------------");
  Serial.printf("Soil Moisture : %.1f %%\n", soilMoisture);
  Serial.printf("Temperature   : %.1f C\n", temperature);
  Serial.printf("Humidity      : %.1f %%\n", humidity);

  // 2. Prepare JSON Payload
  StaticJsonDocument<256> doc;
  doc["device_id"] = DEVICE_ID;
  doc["soil_moisture"] = soilMoisture;
  doc["temperature"] = temperature;
  doc["humidity"] = humidity;

  String jsonString;
  serializeJson(doc, jsonString);

  // 3. Transmit to AWS
  HTTPClient http;
  http.begin(AWS_API_ENDPOINT);
  http.addHeader("Content-Type", "application/json");

  int httpCode = http.POST(jsonString);

  if (httpCode > 0) {
    String response = http.getString();
    Serial.printf("AWS Response [%d]: %s\n", httpCode, response.c_str());
  } else {
    Serial.printf("HTTP POST Error: %s\n", http.errorToString(httpCode).c_str());
  }

  http.end();

  // Transmit reading every 15 seconds
  delay(15000);
}
