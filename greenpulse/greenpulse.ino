#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <time.h>

#include <DHT.h>
#include <Wire.h>
#include <Adafruit_BMP280.h>
#include <U8g2lib.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#include "secrets.h"
#include "certificates.h"

// =====================================================
// PIN DEFINITIONS (EXACTLY AS SPECIFIED - UNCHANGED)
// =====================================================

// ---------- DHT22 ----------
#define DHT_PIN 4
#define DHT_TYPE DHT22

// ---------- Soil Moisture ----------
#define SOIL_PIN 34

// ---------- Air Quality ----------
#define AIR_QUALITY_PIN 35

// ---------- BMP280 / OLED I2C ----------
#define SDA_PIN 21
#define SCL_PIN 22

// ---------- DS18B20 ----------
#define DS18B20_PIN 32

// ---------- LEDs ----------
#define RED_LED 25
#define YELLOW_LED 26
#define GREEN_LED 27


// =====================================================
// SENSOR OBJECTS
// =====================================================

DHT dht(DHT_PIN, DHT_TYPE);

Adafruit_BMP280 bmp;

OneWire oneWire(DS18B20_PIN);
DallasTemperature ds18b20(&oneWire);

U8G2_SH1106_128X64_NONAME_F_HW_I2C oled(
  U8G2_R0,
  U8X8_PIN_NONE
);


// =====================================================
// SENSOR VARIABLES
// =====================================================

float temperature = 0.0;
float humidity = 0.0;

int soilRaw = 0;
float soilPercent = 0.0;

int airQualityRaw = 0;
float airQualityPercent = 0.0;

float pressure = 0.0;

float soilTemperature = 0.0;


// =====================================================
// SOIL SENSOR CALIBRATION
// =====================================================
const int SOIL_DRY_VALUE = 4095;
const int SOIL_WET_VALUE = 1200;


// =====================================================
// AIR QUALITY CALIBRATION
// =====================================================
const int AIR_CLEAN_VALUE = 1000;
const int AIR_BAD_VALUE = 3000;


// =====================================================
// TIMING INTERVALS
// =====================================================

const unsigned long PUBLISH_INTERVAL        = 10000; // Publish telemetry every 10s
const unsigned long MQTT_RECONNECT_INTERVAL = 15000;
const unsigned long WIFI_RECONNECT_INTERVAL = 10000;

const unsigned long SENSOR_INTERVAL         = 2000;  // Periodic sensor read interval (prevents I2C bus lockup)
const unsigned long DHT_INTERVAL            = 2000;  // DHT22 minimum sampling interval
const unsigned long DS18B20_INTERVAL        = 2000;  // Soil temp interval
const unsigned long OLED_UPDATE_INTERVAL    = 500;   // Refresh screen 2x/sec


// =====================================================
// NETWORK OBJECTS
// =====================================================

WiFiClientSecure secureClient;
PubSubClient mqttClient(secureClient);


// =====================================================
// CONNECTION STATUS & TIMERS
// =====================================================

bool mqttConnected = false;

unsigned long lastPublishTime = 0;
unsigned long lastMQTTReconnectAttempt = 0;
unsigned long lastWiFiReconnectAttempt = 0;

unsigned long lastSensorRead = 0;
unsigned long lastDHTRead = 0;
unsigned long lastDS18B20Request = 0;
unsigned long lastDS18B20Conversion = 0;
unsigned long lastOLEDUpdate = 0;

bool ds18b20ConversionStarted = false;


// =====================================================
// FORWARD DECLARATIONS
// =====================================================

void connectToWiFi();
void connectToMQTT();
void syncNTP();

void handleMQTT();
void mqttCallback(char* topic, byte* payload, unsigned int length);

void readDHT22();
void readSoilMoisture();
void readAirQuality();
void readBMP280();
void readDS18B20();

void updatePriorityLEDs();
void updateOLED();

void publishSensorData();

String getUTCTimestamp();


// =====================================================
// SETUP
// =====================================================

void setup() {

  Serial.begin(115200);
  delay(1000);

  Serial.println();
  Serial.println("======================================");
  Serial.println("       GREENPULSE IoT DEVICE");
  Serial.println("======================================");

  // 1. GPIO / LEDs Initialization
  pinMode(RED_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);

  digitalWrite(RED_LED, LOW);
  digitalWrite(YELLOW_LED, LOW);
  digitalWrite(GREEN_LED, LOW);

  // 2. I2C Bus Initialization
  Wire.begin(SDA_PIN, SCL_PIN);

  // 3. DHT22 Initialization
  dht.begin();
  Serial.println("DHT22 initialized.");

  // 4. DS18B20 Initialization (Non-blocking mode configured)
  ds18b20.begin();
  ds18b20.setWaitForConversion(false); // CRITICAL: Avoids 750ms blocking freeze in loop()!
  ds18b20.setResolution(10);           // 10-bit resolution (~187ms conversion time)
  Serial.print("DS18B20 devices found: ");
  Serial.println(ds18b20.getDeviceCount());

  // 5. BMP280 Initialization (Checks both 0x76 and alternate 0x77 I2C addresses)
  if (bmp.begin(0x76) || bmp.begin(0x77)) {
    Serial.println("BMP280 initialized successfully.");
    bmp.setSampling(
      Adafruit_BMP280::MODE_NORMAL,
      Adafruit_BMP280::SAMPLING_X2,
      Adafruit_BMP280::SAMPLING_X16,
      Adafruit_BMP280::FILTER_X16,
      Adafruit_BMP280::STANDBY_MS_500
    );
  } else {
    Serial.println("WARNING: BMP280 not detected on 0x76 or 0x77!");
  }

  // 6. OLED Initialization
  oled.begin();
  oled.clearBuffer();
  oled.setFont(u8g2_font_6x10_tf);
  oled.drawStr(0, 12, "GreenPulse IoT");
  oled.drawStr(0, 28, "Connecting WiFi...");
  oled.drawStr(0, 44, "Please wait");
  oled.sendBuffer();
  Serial.println("OLED initialized.");

  // 7. WiFi & NTP Time Sync
  connectToWiFi();
  syncNTP();

  // 8. AWS TLS Security Configuration (Loaded from certificates.h)
  Serial.println();
  Serial.println("Configuring AWS TLS...");
  secureClient.setCACert(AWS_CERT_CA);
  secureClient.setCertificate(AWS_CERT_CRT);
  secureClient.setPrivateKey(AWS_CERT_PRIVATE);
  Serial.println("AWS TLS certificates loaded successfully.");

  // 9. MQTT Client Setup
  mqttClient.setServer(AWS_IOT_ENDPOINT, AWS_IOT_PORT);
  mqttClient.setCallback(mqttCallback);
  mqttClient.setKeepAlive(120);
  mqttClient.setSocketTimeout(15);
  mqttClient.setBufferSize(2048);

  // 10. Initial MQTT Connection
  connectToMQTT();

  Serial.println();
  Serial.println("======================================");
  Serial.println("GreenPulse initialization complete.");
  Serial.println("======================================");
}


// =====================================================
// MAIN LOOP
// =====================================================

void loop() {

  // 1. Maintain WiFi Connection
  if (WiFi.status() != WL_CONNECTED) {
    mqttConnected = false;
    if (millis() - lastWiFiReconnectAttempt >= WIFI_RECONNECT_INTERVAL) {
      lastWiFiReconnectAttempt = millis();
      connectToWiFi();
    }
    delay(10);
    return;
  }

  // 2. Maintain MQTT Connection & Keepalive
  handleMQTT();

  // 3. Periodic Sensor Readings (DHT, DS18B20, Soil, Air, BMP280)
  readDHT22();
  readDS18B20();

  if (millis() - lastSensorRead >= SENSOR_INTERVAL) {
    lastSensorRead = millis();
    readSoilMoisture();
    readAirQuality();
    readBMP280();
  }

  // 4. Update LEDs according to health priorities
  updatePriorityLEDs();

  // 5. Update OLED Screen
  if (millis() - lastOLEDUpdate >= OLED_UPDATE_INTERVAL) {
    lastOLEDUpdate = millis();
    updateOLED();
  }

  delay(10);
}


// =====================================================
// WIFI CONNECTION & NTP TIME SYNC
// =====================================================

void connectToWiFi() {
  if (WiFi.status() == WL_CONNECTED) {
    return;
  }

  Serial.println();
  Serial.println("======================================");
  Serial.println("Connecting to Wi-Fi...");
  Serial.println("======================================");

  WiFi.mode(WIFI_STA);
  WiFi.setSleep(false);
  WiFi.setAutoReconnect(true);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 40) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Wi-Fi connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
    Serial.print("Wi-Fi RSSI: ");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm");
  } else {
    Serial.println("Wi-Fi connection failed. Will retry periodically.");
  }
}

void syncNTP() {
  Serial.println("Synchronizing NTP Time with pool.ntp.org...");
  configTime(0, 0, "pool.ntp.org", "time.nist.gov");
  
  time_t now = time(nullptr);
  int retry = 0;
  while (now < 100000 && retry < 20) {
    delay(300);
    Serial.print(".");
    now = time(nullptr);
    retry++;
  }
  Serial.println();

  if (now > 100000) {
    Serial.println("[OK] UTC Time synchronized successfully.");
  } else {
    Serial.println("[WARN] NTP sync pending, will retry in background.");
  }
}


// =====================================================
// MQTT CONNECTION (STABLE RECONNECT LOGIC)
// =====================================================

void connectToMQTT() {
  if (WiFi.status() != WL_CONNECTED) {
    return;
  }

  if (mqttClient.connected()) {
    mqttConnected = true;
    return;
  }

  Serial.println();
  Serial.println("======================================");
  Serial.println("Connecting to AWS IoT Core via TLS...");
  Serial.println("======================================");
  Serial.print("Endpoint: ");
  Serial.println(AWS_IOT_ENDPOINT);
  Serial.print("MQTT Client ID: ");
  Serial.println(MQTT_CLIENT_ID);

  bool connected = mqttClient.connect(MQTT_CLIENT_ID);

  if (connected) {
    mqttConnected = true;

    Serial.println();
    Serial.println("======================================");
    Serial.println("AWS IoT MQTT CONNECTED!");
    Serial.println("======================================");

    // Subscribe to topics
    mqttClient.subscribe(MQTT_AI_QUOTE_TOPIC);
    mqttClient.subscribe(MQTT_AI_ALERT_TOPIC);
    mqttClient.subscribe(MQTT_PLANT_STATUS_TOPIC);

    Serial.println("Subscribed to GreenPulse command topics.");
    lastPublishTime = millis();

  } else {
    mqttConnected = false;
    Serial.println();
    Serial.println("AWS IoT MQTT connection FAILED.");
    Serial.print("PubSubClient state: ");
    Serial.println(mqttClient.state());
  }
}


// =====================================================
// MQTT HANDLER
// =====================================================

void handleMQTT() {
  if (mqttClient.connected()) {
    mqttConnected = true;
    mqttClient.loop();

    // Periodic sensor publish
    if (millis() - lastPublishTime >= PUBLISH_INTERVAL) {
      publishSensorData();
      lastPublishTime = millis();
    }
    return;
  }

  if (mqttConnected) {
    mqttConnected = false;
    Serial.println("\n[MQTT] Connection lost. Reconnecting soon...");
  }

  if (millis() - lastMQTTReconnectAttempt >= MQTT_RECONNECT_INTERVAL) {
    lastMQTTReconnectAttempt = millis();
    connectToMQTT();
  }
}


// =====================================================
// MQTT CALLBACK
// =====================================================

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  Serial.println();
  Serial.println("======================================");
  Serial.print("MQTT MESSAGE RECEIVED [");
  Serial.print(topic);
  Serial.println("]:");

  for (unsigned int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
  Serial.println("======================================");
}


// =====================================================
// SENSOR READING FUNCTIONS
// =====================================================

void readDHT22() {
  if (millis() - lastDHTRead < DHT_INTERVAL) {
    return;
  }
  lastDHTRead = millis();

  float newHumidity = dht.readHumidity();
  float newTemperature = dht.readTemperature();

  if (!isnan(newHumidity) && !isnan(newTemperature)) {
    humidity = newHumidity;
    temperature = newTemperature;
  }
}

void readSoilMoisture() {
  long sum = 0;
  for (int i = 0; i < 5; i++) {
    sum += analogRead(SOIL_PIN);
    delayMicroseconds(50);
  }
  soilRaw = sum / 5;

  float mapped = (float)map(soilRaw, SOIL_DRY_VALUE, SOIL_WET_VALUE, 0, 100);
  soilPercent = constrain(mapped, 0.0f, 100.0f);
}

void readAirQuality() {
  long sum = 0;
  for (int i = 0; i < 5; i++) {
    sum += analogRead(AIR_QUALITY_PIN);
    delayMicroseconds(50);
  }
  airQualityRaw = sum / 5;

  float mapped = (float)map(airQualityRaw, AIR_CLEAN_VALUE, AIR_BAD_VALUE, 100, 0);
  airQualityPercent = constrain(mapped, 0.0f, 100.0f);
}

void readBMP280() {
  float p = bmp.readPressure();
  if (!isnan(p) && p > 30000.0f) {
    pressure = p / 100.0F; // Pa to hPa
  }
}

void readDS18B20() {
  // 1. Request conversion periodically
  if (!ds18b20ConversionStarted && (millis() - lastDS18B20Request >= DS18B20_INTERVAL)) {
    lastDS18B20Request = millis();
    ds18b20.requestTemperatures();
    ds18b20ConversionStarted = true;
    lastDS18B20Conversion = millis();
  }

  // 2. Read temperature once 10-bit conversion is ready (~250ms)
  if (ds18b20ConversionStarted && (millis() - lastDS18B20Conversion >= 250)) {
    float newTemperature = ds18b20.getTempCByIndex(0);
    if (newTemperature != DEVICE_DISCONNECTED_C && newTemperature > -40.0f && newTemperature < 100.0f && newTemperature != 85.0f) {
      soilTemperature = newTemperature;
    }
    ds18b20ConversionStarted = false;
  }
}


// =====================================================
// PRIORITY LED SYSTEM
// =====================================================

void updatePriorityLEDs() {
  digitalWrite(RED_LED, LOW);
  digitalWrite(YELLOW_LED, LOW);
  digitalWrite(GREEN_LED, LOW);

  // Critical alert
  if (soilPercent < 20 || temperature > 35 || temperature < 10) {
    digitalWrite(RED_LED, HIGH);
    return;
  }

  // Warning alert
  if (soilPercent < 40 || temperature > 30 || temperature < 15) {
    digitalWrite(YELLOW_LED, HIGH);
    return;
  }

  // Normal status
  digitalWrite(GREEN_LED, HIGH);
}


// =====================================================
// OLED DISPLAY
// =====================================================

void updateOLED() {
  oled.clearBuffer();
  oled.setFont(u8g2_font_6x10_tf);

  // Line 1: Ambient Temp & Humidity
  oled.setCursor(0, 10);
  oled.print("T:");
  oled.print(temperature, 1);
  oled.print("C  H:");
  oled.print(humidity, 0);
  oled.print("%");

  // Line 2: Soil Moisture
  oled.setCursor(0, 21);
  oled.print("Soil:");
  oled.print(soilPercent, 0);
  oled.print("%");

  // Line 3: Air Quality Indicator
  oled.setCursor(0, 32);
  oled.print("Air:");
  oled.print(airQualityPercent, 0);
  oled.print("%");

  // Line 4: Barometric Pressure
  oled.setCursor(0, 43);
  oled.print("P:");
  oled.print(pressure, 0);
  oled.print("hPa");

  // Line 5: Soil Temperature (DS18B20)
  oled.setCursor(0, 54);
  oled.print("SoilT:");
  oled.print(soilTemperature, 1);
  oled.print("C");

  // Line 6: MQTT Status
  oled.setCursor(0, 63);
  oled.print("MQTT:");
  if (mqttClient.connected()) {
    oled.print("CONNECTED");
  } else {
    oled.print("OFFLINE");
  }

  oled.sendBuffer();
}


// =====================================================
// PUBLISH SENSOR DATA (100% AWS IOT COMPLIANT)
// =====================================================

void publishSensorData() {
  if (!mqttClient.connected()) {
    Serial.println("[MQTT] Publish skipped: MQTT is disconnected.");
    return;
  }

  JsonDocument doc;

  doc["device_id"]           = MQTT_CLIENT_ID;
  doc["timestamp"]           = getUTCTimestamp();
  doc["temperature"]         = round(temperature * 10.0f) / 10.0f;
  doc["humidity"]            = round(humidity * 10.0f) / 10.0f;
  doc["soil_moisture"]       = round(soilPercent * 10.0f) / 10.0f;
  doc["soil_temperature"]    = round(soilTemperature * 10.0f) / 10.0f;
  doc["air_quality_percent"] = round(airQualityPercent * 10.0f) / 10.0f;
  doc["air_pressure"]        = round(pressure * 10.0f) / 10.0f;

  char jsonBuffer[512];
  serializeJson(doc, jsonBuffer, sizeof(jsonBuffer));

  Serial.println();
  Serial.println("--- PUBLISHING SENSOR DATA ---");
  Serial.print("Topic: ");
  Serial.println(MQTT_SENSOR_TOPIC);
  Serial.print("Payload: ");
  Serial.println(jsonBuffer);

  // Calling publish without length variable prevents PubSubClient from converting
  // length into 'retained = true', ensuring stable 100% connection with AWS IoT Core.
  bool success = mqttClient.publish(MQTT_SENSOR_TOPIC, jsonBuffer);

  if (success) {
    Serial.println("MQTT Publish: SUCCESS");
  } else {
    Serial.println("MQTT Publish: FAILED");
    Serial.print("PubSubClient state: ");
    Serial.println(mqttClient.state());
  }
}


// =====================================================
// UTC TIMESTAMP
// =====================================================

String getUTCTimestamp() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo, 500)) {
    time_t now = time(nullptr);
    if (now > 100000) {
      gmtime_r(&now, &timeinfo);
      char timestamp[30];
      strftime(timestamp, sizeof(timestamp), "%Y-%m-%dT%H:%M:%SZ", &timeinfo);
      return String(timestamp);
    }
    return "1970-01-01T00:00:00Z";
  }

  char timestamp[30];
  strftime(timestamp, sizeof(timestamp), "%Y-%m-%dT%H:%M:%SZ", &timeinfo);
  return String(timestamp);
}
