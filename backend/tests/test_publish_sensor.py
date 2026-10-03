import json
import paho.mqtt.client as mqtt


MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "greenpulse/sensor/data"


sensor_data = {
    "device_id": "greenpulse-001",
    "timestamp": "2026-10-03T08:30:00Z",
    "soil_moisture": 45.5,
    "temperature": 27.2,
    "humidity": 65.0
}


payload = json.dumps(sensor_data)


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.connect(
    MQTT_BROKER,
    MQTT_PORT,
    60
)

client.publish(
    MQTT_TOPIC,
    payload
)

client.disconnect()


print("Test sensor data published successfully.")
print(payload)