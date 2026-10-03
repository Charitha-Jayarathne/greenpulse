import json
import random
import time

import paho.mqtt.client as mqtt


MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "greenpulse/sensor/data"

DEVICE_ID = "greenpulse-001"


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect(MQTT_BROKER, MQTT_PORT, 60)

print("Connected to MQTT broker")
print("Starting GreenPulse sensor simulator...")


while True:
    sensor_data = {
        "device_id": DEVICE_ID,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "soil_moisture": round(random.uniform(20, 80), 1),
        "temperature": round(random.uniform(20, 35), 1),
        "humidity": round(random.uniform(40, 80), 1)
    }

    payload = json.dumps(sensor_data)

    client.publish(MQTT_TOPIC, payload)

    print(f"Published: {payload}")

    time.sleep(5)