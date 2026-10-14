#ifndef SECRETS_H
#define SECRETS_H

// =====================================================
// 1. Wi-Fi Configuration
// =====================================================
const char WIFI_SSID[]     = "Dialog 4G 714";
const char WIFI_PASSWORD[] = "67D3ddcD";

// =====================================================
// 2. AWS IoT Core Endpoint & Device Identifiers
// =====================================================
const char AWS_IOT_ENDPOINT[] = "a379y9x438krnt-ats.iot.us-east-1.amazonaws.com";
const int  AWS_IOT_PORT       = 8883;

#define MQTT_CLIENT_ID "greenpulse-team-infinix"
const char DEVICE_ID[] = "greenpulse-team-infinix";

// =====================================================
// 3. MQTT Topics
// =====================================================
#define MQTT_SENSOR_TOPIC       "greenpulse/sensor/data"
#define MQTT_AI_QUOTE_TOPIC     "greenpulse/ai/quote"
#define MQTT_AI_ALERT_TOPIC     "greenpulse/ai/alert"
#define MQTT_PLANT_STATUS_TOPIC "greenpulse/plant/status"

#endif // SECRETS_H
