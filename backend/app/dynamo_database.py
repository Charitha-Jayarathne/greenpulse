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


def get_historical_readings(device_id="greenpulse-team-infinix", time_range="24h", target_points=30):
    """
    Retrieve historical telemetry for a device over 24h, 7d, or 30d.
    Downsamples to `target_points` for smooth, high-performance chart rendering.
    Calculates summary analytics (min, max, avg, drying trend).
    """
    from datetime import datetime, timezone, timedelta

    now = datetime.now(timezone.utc)
    if time_range == "30d":
        cutoff = (now - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
        time_format = "%m/%d %H:%M"
    elif time_range == "7d":
        cutoff = (now - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
        time_format = "%a %H:%M"
    else:  # 24h default
        cutoff = (now - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")
        time_format = "%H:%M"

    items = []
    try:
        # First query with cutoff
        resp = readings_table.query(
            KeyConditionExpression=Key("device_id").eq(str(device_id)) & Key("timestamp").gte(cutoff),
            ScanIndexForward=True,
            Limit=500
        )
        items = resp.get("Items", [])
    except Exception as e:
        print(f"[DYNAMO] Range query error: {e}")

    # Fallback: if no items in exact window (e.g., timezone gap or device off), get latest 150 items
    if len(items) < 5:
        try:
            resp_fallback = readings_table.query(
                KeyConditionExpression=Key("device_id").eq(str(device_id)),
                ScanIndexForward=False,
                Limit=150
            )
            items = list(reversed(resp_fallback.get("Items", [])))
        except Exception as e:
            print(f"[DYNAMO] Fallback query error: {e}")

    if not items:
        return {
            "success": False,
            "device_id": device_id,
            "range": time_range,
            "count": 0,
            "stats": {},
            "data": []
        }

    total_found = len(items)

    # Downsampling to target_points
    if total_found <= target_points:
        sampled_items = items
    else:
        step = total_found / float(target_points)
        sampled_indices = [int(i * step) for i in range(target_points)]
        sampled_items = [items[idx] for idx in sampled_indices if idx < total_found]

    formatted_points = []
    moistures = []
    temps = []
    humidities = []

    for it in sampled_items:
        ts_raw = it.get("timestamp", "")
        # Format label
        label = ts_raw
        try:
            dt = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
            label = dt.strftime(time_format)
        except Exception:
            if len(ts_raw) >= 16:
                label = ts_raw[11:16]

        m = float(it.get("soil_moisture", 0))
        st = float(it.get("soil_temperature", it.get("temperature", 24)))
        t = float(it.get("temperature", 25))
        h = float(it.get("humidity", 50))
        p = float(it.get("air_pressure", 1012))

        moistures.append(m)
        temps.append(t)
        humidities.append(h)

        formatted_points.append({
            "timestamp": ts_raw,
            "time_label": label,
            "soil_moisture": round(m, 1),
            "soil_temperature": round(st, 1),
            "temperature": round(t, 1),
            "humidity": round(h, 1),
            "air_pressure": round(p, 1)
        })

    # Summary Statistics
    avg_m = round(sum(moistures) / len(moistures), 1) if moistures else 0
    min_m = round(min(moistures), 1) if moistures else 0
    max_m = round(max(moistures), 1) if moistures else 0
    avg_t = round(sum(temps) / len(temps), 1) if temps else 0
    max_t = round(max(temps), 1) if temps else 0
    avg_h = round(sum(humidities) / len(humidities), 1) if humidities else 0

    # Trend calculation
    first_m = moistures[0] if moistures else avg_m
    last_m = moistures[-1] if moistures else avg_m
    diff_m = last_m - first_m
    if diff_m < -2.0:
        drying_trend = f"Drying ({diff_m:+.1f}%)"
    elif diff_m > 2.0:
        drying_trend = f"Hydrating ({diff_m:+.1f}%)"
    else:
        drying_trend = "Stable Moisture"

    stats = {
        "avg_moisture": avg_m,
        "min_moisture": min_m,
        "max_moisture": max_m,
        "avg_temp": avg_t,
        "max_temp": max_t,
        "avg_humidity": avg_h,
        "drying_trend": drying_trend,
        "total_records_analyzed": total_found
    }

    return {
        "success": True,
        "device_id": device_id,
        "range": time_range,
        "count": len(formatted_points),
        "stats": stats,
        "data": formatted_points
    }


def display_device_dashboard(device_id="greenpulse-001"):
    """Fetch and print summary status from DynamoDB."""
    print("=" * 60)
    print(f"[DASHBOARD] GreenPulse Cloud Dashboard - Device: {device_id}")
    print("=" * 60)

    reading = get_latest_reading(device_id)
    assessment = get_latest_assessment(device_id)

    if not reading and not assessment:
        print("No data found in DynamoDB for this device.")
        return

    if reading:
        print(f"Timestamp    : {reading.get('timestamp')}")
        print(f"Soil Moisture: {reading.get('soil_moisture')}%")
        print(f"Temperature  : {reading.get('temperature')} C")
        print(f"Humidity     : {reading.get('humidity')}%")

    if assessment:
        print("-" * 60)
        print(f"Status   : {assessment.get('status')} ({assessment.get('urgency')} Urgency)")
        print(f"Message  : {assessment.get('message')}")
        print(f"Trend    : {assessment.get('moisture_trend', 'N/A')}")
    print("=" * 60)


if __name__ == "__main__":
    display_device_dashboard("greenpulse-team-infinix")

