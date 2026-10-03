import paho.mqtt.client as mqtt


MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_AI_QUOTE_TOPIC = "greenpulse/ai/quote"


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)


print("Connecting to MQTT broker...")

client.connect(
    MQTT_BROKER,
    MQTT_PORT,
    60
)


test_message = (
    "GreenPulse test: "
    "The plant is currently healthy. "
    "Continue monitoring soil moisture."
)


client.publish(
    MQTT_AI_QUOTE_TOPIC,
    test_message
)


print(
    f"Test AI advice published to: "
    f"{MQTT_AI_QUOTE_TOPIC}"
)


client.disconnect()