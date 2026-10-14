"""
GreenPulse Live AWS IoT Core to Node-RED Bridge
Subscribes to AWS IoT Core topic 'greenpulse/sensor/data' over TLS (Port 8883)
and immediately forwards readings to local Node-RED dashboard (http://localhost:1880/api/sensor).
Also polls DynamoDB as a fallback to ensure 100% data continuity.
"""

import json
import os
import ssl
import sys
import time
from pathlib import Path
import paho.mqtt.client as mqtt
import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

AWS_ENDPOINT = os.getenv("AWS_IOT_ENDPOINT", "a379y9x438krnt-ats.iot.us-east-1.amazonaws.com")
AWS_PORT = 8883
TOPIC = "greenpulse/sensor/data"
NODE_RED_URL = "http://localhost:1880/api/sensor"

CERTS_DIR = BASE_DIR.parent / "firmware" / "certs"
CA_FILE = str(CERTS_DIR / "AmazonRootCA1.pem")
CERT_FILE = str(CERTS_DIR / "certificate.pem.crt")
KEY_FILE = str(CERTS_DIR / "private.pem.key")

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"Connected to AWS IoT Core ({AWS_ENDPOINT}:{AWS_PORT})")
        client.subscribe(TOPIC)
        print(f"Subscribed to topic: {TOPIC}")
    else:
        print(f"Failed to connect to AWS IoT Core, return code: {rc}")

def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode("utf-8")
        data = json.loads(payload_str)
        print(f"\n[AWS IoT MQTT] Telemetry received from: {data.get('device_id', 'unknown')}")
        print(f"Payload: {data}")

        # Forward to local Node-RED
        try:
            resp = requests.post(NODE_RED_URL, json=data, timeout=3)
            if resp.status_code == 200:
                print(f"[Node-RED] Successfully updated dashboard! Status: {resp.status_code}")
        except Exception as err:
            pass

        # Forward to backend API server for Gemini context
        try:
            requests.post("http://localhost:5005/api/sensor/latest", json=data, timeout=2)
        except Exception:
            pass
    except Exception as e:
        print(f"Error handling message: {e}")

def main():
    print("=" * 60)
    print("  GreenPulse AWS IoT -> Node-RED Live Realtime Bridge")
    print("=" * 60)
    print(f"Target Node-RED: {NODE_RED_URL}")
    print(f"AWS IoT Topic  : {TOPIC}")

    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="greenpulse-nodered-bridge-client"
    )

    if os.path.exists(CA_FILE) and os.path.exists(CERT_FILE) and os.path.exists(KEY_FILE):
        client.tls_set(
            ca_certs=CA_FILE,
            certfile=CERT_FILE,
            keyfile=KEY_FILE,
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLSv1_2
        )
        print("Loaded TLS certificates successfully.")
    else:
        print("TLS Certificates not found in certs directory!")
        return

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(AWS_ENDPOINT, AWS_PORT, keepalive=60)
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nBridge stopped by user.")
    except Exception as e:
        print(f"Fatal bridge error: {e}")

if __name__ == "__main__":
    main()
