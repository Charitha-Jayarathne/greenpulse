"""
GreenPulse Daily AI Plant Health Analyzer
Aggregates full-day sensor telemetry and periodic diagnoses,
prompts Google Gemini AI, and generates a comprehensive 24-hour plant care report.
"""

import json
import os
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
import boto3
from boto3.dynamodb.conditions import Key
import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
readings_table = dynamodb.Table("greenpulse_sensor_readings")
devices_table = dynamodb.Table("greenpulse_devices")
advice_table = dynamodb.Table("greenpulse_ai_advice")


def fetch_day_telemetry(device_id, target_date=None):
    """
    Fetch all readings for a specific date (YYYY-MM-DD). Defaults to today (UTC).
    """
    if not target_date:
        target_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    try:
        response = readings_table.query(
            KeyConditionExpression=Key("device_id").eq(str(device_id)) & Key("timestamp").begins_with(target_date),
            ScanIndexForward=True,  # Chronological order
        )
        return response.get("Items", []), target_date
    except Exception as e:
        print(f"[ANALYZER] Error fetching day telemetry: {e}")
        return [], target_date


def calculate_daily_statistics(items, min_moisture=30.0, max_moisture=70.0):
    """Calculate key mathematical metrics across the 24-hour period."""
    if not items:
        return None

    moistures = [float(x["soil_moisture"]) for x in items]
    temps = [float(x["temperature"]) for x in items]
    humidities = [float(x["humidity"]) for x in items]

    dry_count = sum(1 for m in moistures if m < min_moisture)
    overwatered_count = sum(1 for m in moistures if m > max_moisture)
    optimal_count = len(moistures) - (dry_count + overwatered_count)

    return {
        "readings_count": len(items),
        "avg_moisture": round(sum(moistures) / len(moistures), 1),
        "min_moisture": round(min(moistures), 1),
        "max_moisture": round(max(moistures), 1),
        "avg_temp": round(sum(temps) / len(temps), 1),
        "max_temp": round(max(temps), 1),
        "min_temp": round(min(temps), 1),
        "avg_humidity": round(sum(humidities) / len(humidities), 1),
        "optimal_percentage": round((optimal_count / len(items)) * 100, 1),
        "dry_percentage": round((dry_count / len(items)) * 100, 1),
        "overwatered_percentage": round((overwatered_count / len(items)) * 100, 1),
        "first_timestamp": items[0]["timestamp"],
        "latest_timestamp": items[-1]["timestamp"],
    }


def call_gemini(prompt):
    """Direct HTTP call to Google Gemini API (gemini-flash-latest)."""
    if not GOOGLE_API_KEY:
        return "Error: GOOGLE_API_KEY not configured in .env."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={GOOGLE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 800}
    }

    try:
        res = requests.post(url, headers=headers, json=body, timeout=25)
        if res.status_code == 200:
            data = res.json()
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        else:
            return f"Gemini API returned code {res.status_code}: {res.text[:200]}"
    except Exception as e:
        return f"Gemini invocation error: {str(e)}"


def generate_full_day_report(device_id="greenpulse-001", target_date=None):
    """
    Main function: Aggregates day data, invokes Gemini AI,
    saves the final report in DynamoDB, and returns structured summary.
    """
    print(f"\n[ANALYZER] Generating full-day analysis for device: {device_id}...")

    # 1. Fetch active plant details
    try:
        dev_res = devices_table.get_item(Key={"device_id": str(device_id)})
        device = dev_res.get("Item", {})
        plant_name = device.get("plant_name", "Rose")
        location = device.get("location_name", "Kurunegala")
        min_m = float(device.get("min_moisture", 30))
        max_m = float(device.get("max_moisture", 70))
    except Exception:
        plant_name = "Rose"
        location = "Kurunegala"
        min_m, max_m = 30.0, 70.0

    # 2. Fetch day's data
    items, date_str = fetch_day_telemetry(device_id, target_date)

    if not items:
        # Fallback to recent readings if no data specifically on target_date
        response = readings_table.query(
            KeyConditionExpression=Key("device_id").eq(str(device_id)),
            ScanIndexForward=False,
            Limit=20,
        )
        items = list(reversed(response.get("Items", [])))

    if not items:
        return {"error": "No sensor readings found in DynamoDB for this device to analyze."}

    # 3. Calculate metrics
    stats = calculate_daily_statistics(items, min_m, max_m)

    # 4. Construct prompt for Gemini
    prompt = f"""
You are the GreenPulse Chief Agronomist and Senior Plant Care AI.

Analyze this 24-hour environmental telemetry summary for a plant and provide a comprehensive Full-Day Care Review.

PLANT PROFILE:
- Plant Species: {plant_name}
- Location: {location}
- Healthy Soil Moisture Range: {min_m}% - {max_m}%
- Target Date: {date_str}

FULL-DAY SENSOR METRICS (Based on {stats['readings_count']} recorded readings):
- Average Soil Moisture: {stats['avg_moisture']}% (Min: {stats['min_moisture']}%, Max: {stats['max_moisture']}%)
- Optimal Moisture Duration: {stats['optimal_percentage']}% of the day
- Under-watered / Dry Duration: {stats['dry_percentage']}% of the day
- Over-watered Duration: {stats['overwatered_percentage']}% of the day
- Temperature Range: {stats['min_temp']}°C to {stats['max_temp']}°C (Average: {stats['avg_temp']}°C)
- Average Relative Humidity: {stats['avg_humidity']}%

Please format your response clearly in markdown with these exact 4 sections:
1. **Daily Health Grade**: Give a letter grade (e.g. A, B+, C) and a 1-sentence verdict.
2. **24-Hour Environmental Analysis**: How did the plant respond to today's temperature, moisture curve, and humidity?
3. **Hydration & Root Health**: Was watering timely and sufficient? Any risk of root rot or drought stress?
4. **Actionable Recommendations for Tomorrow**: 2-3 specific, practical steps the owner should take tomorrow morning/afternoon.
"""

    print("[ANALYZER] Calling Google Gemini for comprehensive daily report...")
    ai_report = call_gemini(prompt)

    # 5. Save Report to DynamoDB
    timestamp_now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        advice_table.put_item(
            Item={
                "device_id": str(device_id),
                "timestamp": timestamp_now,
                "date": date_str,
                "type": "DAILY_SUMMARY",
                "plant_name": plant_name,
                "location": location,
                "avg_moisture": Decimal(str(stats["avg_moisture"])),
                "avg_temp": Decimal(str(stats["avg_temp"])),
                "report": ai_report
            }
        )
        print("[ANALYZER] Full-day AI report successfully saved to DynamoDB 'greenpulse_ai_advice'!")
    except Exception as e:
        print(f"[ANALYZER] Warning: Could not save report to DynamoDB: {e}")

    return {
        "success": True,
        "device_id": device_id,
        "plant_name": plant_name,
        "location": location,
        "date": date_str,
        "timestamp": timestamp_now,
        "stats": stats,
        "report": ai_report
    }


if __name__ == "__main__":
    result = generate_full_day_report("greenpulse-001")
    print("\n" + "=" * 60)
    print("[REPORT] FULL-DAY AI PLANT REPORT:")
    print("=" * 60)
    # Encode with replacement for safe terminal display on Windows
    report_text = result.get("report", "")
    print(report_text.encode('ascii', errors='replace').decode('ascii'))
