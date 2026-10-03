"""
GreenPulse DynamoDB Service Layer
Provides utility functions to read sensor history, device settings,
and plant assessments directly from AWS DynamoDB.
"""

import os
from decimal import Decimal
from pathlib import Path
import boto3
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)

readings_table = dynamodb.Table("greenpulse_sensor_readings")
devices_table = dynamodb.Table("greenpulse_devices")
assessments_table = dynamodb.Table("greenpulse_assessments")
advice_table = dynamodb.Table("greenpulse_ai_advice")


def get_latest_reading(device_id):
    """Retrieve the most recent sensor reading for a device."""
    try:
        response = readings_table.query(
            KeyConditionExpression=Key("device_id").eq(str(device_id)),
            ScanIndexForward=False,
            Limit=1,
        )
        items = response.get("Items", [])
        return items[0] if items else None
    except Exception as e:
        print(f"Error querying latest reading: {e}")
        return None


def get_recent_readings(device_id, limit=10):
    """Retrieve the last N sensor readings for a device."""
    try:
        response = readings_table.query(
            KeyConditionExpression=Key("device_id").eq(str(device_id)),
            ScanIndexForward=False,
            Limit=limit,
        )
        return response.get("Items", [])
    except Exception as e:
        print(f"Error querying recent readings: {e}")
        return []


def get_latest_assessment(device_id):
    """Retrieve the most recent health diagnosis for a device."""
    try:
        response = assessments_table.query(
            KeyConditionExpression=Key("device_id").eq(str(device_id)),
            ScanIndexForward=False,
            Limit=1,
        )
        items = response.get("Items", [])
        return items[0] if items else None
    except Exception as e:
        print(f"Error querying latest assessment: {e}")
        return None


def display_device_dashboard(device_id="greenpulse-001"):
    """Fetch and print summary status from DynamoDB."""
    print("=" * 60)
    print(f"📊 GreenPulse Cloud Dashboard — Device: {device_id}")
    print("=" * 60)

    reading = get_latest_reading(device_id)
    assessment = get_latest_assessment(device_id)

    if not reading and not assessment:
        print("No data found in DynamoDB for this device.")
        return

    if reading:
        print(f"🕒 Timestamp    : {reading.get('timestamp')}")
        print(f"🌱 Soil Moisture: {reading.get('soil_moisture')}%")
        print(f"🌡 Temperature  : {reading.get('temperature')}°C")
        print(f"💧 Humidity     : {reading.get('humidity')}%")

    if assessment:
        print("-" * 60)
        print(f"Status   : {assessment.get('status')} ({assessment.get('urgency')} Urgency)")
        print(f"Message  : {assessment.get('message')}")
        print(f"Trend    : {assessment.get('moisture_trend', 'N/A')}")
    print("=" * 60)


if __name__ == "__main__":
    display_device_dashboard("greenpulse-001")
