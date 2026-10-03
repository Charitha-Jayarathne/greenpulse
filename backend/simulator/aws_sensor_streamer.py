"""
GreenPulse Automated Sensor Streamer for AWS Lambda & DynamoDB
Simulates real plant sensor behavior and streams telemetry to AWS.
"""

import json
import os
import random
import time
from datetime import datetime, timezone
from pathlib import Path
import boto3
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
FUNCTION_NAME = os.getenv("LAMBDA_FUNCTION_NAME", "greenpulse-process-sensor")
DEVICE_ID = os.getenv("DEVICE_ID", "greenpulse-001")

# Initialize Lambda Client
lambda_client = boto3.client("lambda", region_name=AWS_REGION)


class PlantSensorSimulator:
    """Simulates realistic plant dynamics over time."""

    def __init__(self, initial_moisture=55.0, initial_temp=27.0, initial_humidity=65.0):
        self.moisture = initial_moisture
        self.temperature = initial_temp
        self.humidity = initial_humidity
        self.cycle_count = 0

    def step(self):
        """Simulate next reading with natural variations."""
        self.cycle_count += 1

        # Simulate gradual drying, with occasional automatic watering
        if self.moisture < 22.0:
            # Simulated watering event!
            print("\n💧 [EVENT] Plant was watered! Soil moisture jumping up.")
            self.moisture += random.uniform(35.0, 45.0)
        else:
            # Natural drying (-0.8% to -2.0% per cycle)
            self.moisture -= random.uniform(0.8, 2.0)

        # Natural temperature fluctuations (24°C - 35°C)
        self.temperature += random.uniform(-0.5, 0.6)
        self.temperature = max(22.0, min(36.0, self.temperature))

        # Humidity correlated with moisture
        self.humidity += random.uniform(-1.0, 1.0)
        self.humidity = max(35.0, min(85.0, self.humidity))

        # Return sanitized reading
        return {
            "device_id": DEVICE_ID,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "soil_moisture": round(self.moisture, 1),
            "temperature": round(self.temperature, 1),
            "humidity": round(self.humidity, 1),
        }


def stream_to_aws(interval_seconds=5, max_readings=None):
    """Continuously transmits simulated sensor telemetry to AWS Lambda."""
    sim = PlantSensorSimulator()

    print("=" * 65)
    print("🌿 GreenPulse AWS Sensor Streamer Active")
    print(f"Target Lambda: {FUNCTION_NAME} ({AWS_REGION})")
    print(f"Target Device: {DEVICE_ID}")
    print(f"Interval     : Every {interval_seconds} seconds")
    print("Press Ctrl + C anytime to stop.")
    print("=" * 65)

    count = 0
    try:
        while True:
            count += 1
            reading = sim.step()

            print(f"\n[#{count}] Sending Telemetry:")
            print(f"     Soil Moisture : {reading['soil_moisture']}%")
            print(f"     Temperature   : {reading['temperature']}°C")
            print(f"     Humidity      : {reading['humidity']}%")

            # Call AWS Lambda synchronously to inspect the return diagnosis
            response = lambda_client.invoke(
                FunctionName=FUNCTION_NAME,
                InvocationType="RequestResponse",
                Payload=json.dumps(reading),
            )

            res_payload = json.loads(response["Payload"].read().decode("utf-8"))

            if "body" in res_payload and isinstance(res_payload["body"], str):
                body = json.loads(res_payload["body"])
                status = body.get("status", "UNKNOWN")
                urgency = body.get("urgency", "UNKNOWN")
                msg = body.get("message", "")
                trend = body.get("moisture_trend", "STABLE")

                # Visual status indicator
                indicator = "🟢" if status == "HEALTHY" else ("🟡" if status == "MONITOR" else "🔴")
                print(f"     Lambda Result : {indicator} [{status}] (Urgency: {urgency})")
                print(f"     Trend         : {trend}")
                print(f"     Advice        : {msg}")
            else:
                print(f"     Response      : {res_payload}")

            if max_readings and count >= max_readings:
                print("\nReached requested reading count. Done.")
                break

            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        print("\n\n⏹ Sensor stream stopped by user.")


if __name__ == "__main__":
    stream_to_aws(interval_seconds=5)
