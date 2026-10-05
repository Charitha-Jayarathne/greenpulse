"""
GreenPulse Dual Streamer:
Streams simulated plant sensor telemetry simultaneously to:
1. Local Node-RED Dashboard (http://localhost:1880/api/sensor)
2. AWS Lambda & DynamoDB (via boto3)
"""

import json
import os
import random
import time
from datetime import datetime, timezone
from pathlib import Path
import boto3
import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
FUNCTION_NAME = os.getenv("LAMBDA_FUNCTION_NAME", "greenpulse-process-sensor")
DEVICE_ID = "greenpulse-001"
NODE_RED_URL = "http://localhost:1880/api/sensor"

# Initialize AWS Lambda Client
try:
    lambda_client = boto3.client("lambda", region_name=AWS_REGION)
    aws_available = True
except Exception as e:
    print(f"Warning: AWS Client initialization skipped: {e}")
    aws_available = False


def simulate_and_stream(interval_seconds=4):
    print("=" * 65)
    print("🌿 GreenPulse Live Streamer -> Node-RED + AWS DynamoDB")
    print(f"Node-RED UI : http://localhost:1880/ui")
    print(f"AWS Lambda  : {FUNCTION_NAME} ({AWS_REGION})")
    print(f"Interval    : Every {interval_seconds} seconds")
    print("Press Ctrl + C to stop.")
    print("=" * 65)

    # Initial moisture
    moisture = 55.0
    temp = 27.0
    humidity = 65.0
    reading_count = 0

    try:
        while True:
            reading_count += 1

            # Simulate realistic plant life cycle
            if moisture < 22.0:
                print("\n💧 [EVENT] Plant was watered! Moisture jumping up.")
                moisture += random.uniform(35.0, 45.0)
            else:
                moisture -= random.uniform(0.8, 1.8)

            temp += random.uniform(-0.4, 0.5)
            temp = max(22.0, min(36.0, temp))

            humidity += random.uniform(-1.0, 1.0)
            humidity = max(35.0, min(80.0, humidity))

            telemetry = {
                "device_id": DEVICE_ID,
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "soil_moisture": round(moisture, 1),
                "temperature": round(temp, 1),
                "humidity": round(humidity, 1),
            }

            print(f"\n[#{reading_count}] Reading: {telemetry['soil_moisture']}% moisture | {telemetry['temperature']}C | {telemetry['humidity']}% hum")

            # 1. Send to Node-RED Dashboard via HTTP POST
            try:
                nr_res = requests.post(NODE_RED_URL, json=telemetry, timeout=2)
                if nr_res.status_code == 200:
                    print("     [NODE-RED] ✅ Gauges & Chart Updated Live on UI!")
            except Exception as nr_err:
                print(f"     [NODE-RED] (Offline or waiting) {nr_err}")

            # 2. Send to AWS Lambda & DynamoDB
            if aws_available:
                try:
                    aws_res = lambda_client.invoke(
                        FunctionName=FUNCTION_NAME,
                        InvocationType="RequestResponse",
                        Payload=json.dumps(telemetry),
                    )
                    payload_raw = aws_res["Payload"].read().decode("utf-8")
                    aws_data = json.loads(payload_raw)
                    if "body" in aws_data:
                        body_obj = json.loads(aws_data["body"])
                        status = body_obj.get("status", "OK")
                        print(f"     [AWS CLOUD] ✅ Saved to DynamoDB! Status: {status}")
                except Exception as aws_err:
                    print(f"     [AWS CLOUD] Error: {aws_err}")

            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        print("\n\n⏹ Streaming stopped.")


if __name__ == "__main__":
    simulate_and_stream(interval_seconds=4)
