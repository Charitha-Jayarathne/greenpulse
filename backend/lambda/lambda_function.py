import json
import os
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key

# -------------------------------------------------------------
# DynamoDB Initialization
# -------------------------------------------------------------
dynamodb = boto3.resource("dynamodb")

READINGS_TABLE = os.environ.get("READINGS_TABLE", "greenpulse_sensor_readings")
DEVICES_TABLE = os.environ.get("DEVICES_TABLE", "greenpulse_devices")
ASSESSMENTS_TABLE = os.environ.get("ASSESSMENTS_TABLE", "greenpulse_assessments")

readings_table = dynamodb.Table(READINGS_TABLE)
devices_table = dynamodb.Table(DEVICES_TABLE)
assessments_table = dynamodb.Table(ASSESSMENTS_TABLE)


def get_device_config(device_id):
    """Fetch plant metadata and moisture thresholds from DynamoDB."""
    try:
        response = devices_table.get_item(Key={"device_id": str(device_id)})
        item = response.get("Item")
        if item:
            return {
                "plant_name": item.get("plant_name", "Rose"),
                "location_name": item.get("location_name", "Kurunegala"),
                "min_moisture": float(item.get("min_moisture", 30)),
                "max_moisture": float(item.get("max_moisture", 70)),
            }
    except Exception as e:
        print(f"Warning: Could not fetch device config for {device_id}: {e}")

    # Sensible defaults if not found
    return {
        "plant_name": "General Plant",
        "location_name": "Kurunegala",
        "min_moisture": 30.0,
        "max_moisture": 70.0,
    }


def get_moisture_trend(device_id, limit=5):
    """Calculate trend from the recent readings in DynamoDB."""
    try:
        response = readings_table.query(
            KeyConditionExpression=Key("device_id").eq(str(device_id)),
            ScanIndexForward=False,  # Newest first
            Limit=limit,
        )
        items = response.get("Items", [])
        if len(items) < 2:
            return "STABLE"

        newest = float(items[0]["soil_moisture"])
        oldest = float(items[-1]["soil_moisture"])
        diff = newest - oldest

        if diff > 3.0:
            return "INCREASING"
        elif diff < -3.0:
            return "DECREASING"
        return "STABLE"
    except Exception as e:
        print(f"Trend calculation fallback to STABLE: {e}")
        return "STABLE"


def evaluate_plant_condition(
    soil_moisture,
    temperature,
    humidity,
    moisture_trend="STABLE",
    min_moisture=30,
    max_moisture=70,
):
    """GreenPulse Decision Engine Rules."""
    # Low soil moisture
    if soil_moisture < min_moisture:
        if moisture_trend == "INCREASING":
            return {
                "status": "MONITOR",
                "urgency": "LOW",
                "message": "Soil moisture is low but increasing (watering detected).",
            }
        return {
            "status": "WATER_NEEDED",
            "urgency": "HIGH",
            "message": "Soil moisture is below minimum threshold. Watering required.",
        }

    # Heat stress combined with moderate dryness
    if temperature >= 33 and soil_moisture < 45:
        return {
            "status": "URGENT_CARE",
            "urgency": "HIGH",
            "message": "High temperature and drying soil detected. Shade or hydration needed.",
        }

    # Overwatered
    if soil_moisture > max_moisture:
        return {
            "status": "OVERWATERED",
            "urgency": "MEDIUM",
            "message": "Soil moisture is above maximum safe range. Pause watering.",
        }

    # Healthy optimal range
    if min_moisture <= soil_moisture <= max_moisture and temperature < 33:
        return {
            "status": "HEALTHY",
            "urgency": "LOW",
            "message": "Plant conditions are healthy and well-balanced.",
        }

    return {
        "status": "MONITOR",
        "urgency": "MEDIUM",
        "message": "Plant condition should be observed.",
    }


def lambda_handler(event, context):
    """
    Main AWS Lambda entry point.
    Receives sensor readings, updates DynamoDB, evaluates plant health.
    """
    print("Received event:", json.dumps(event))

    try:
        # Handle payloads whether passed directly or via API Gateway / IoT Rule
        body = event
        if "body" in event and isinstance(event["body"], str):
            body = json.loads(event["body"])

        device_id = str(body["device_id"])
        timestamp = str(body["timestamp"])
        soil_moisture = float(body["soil_moisture"])
        temperature = float(body["temperature"])
        humidity = float(body["humidity"])

        # 1. Fetch Device Configuration from DynamoDB
        device_cfg = get_device_config(device_id)

        # 2. Save Raw Reading to DynamoDB
        readings_table.put_item(
            Item={
                "device_id": device_id,
                "timestamp": timestamp,
                "soil_moisture": Decimal(str(round(soil_moisture, 2))),
                "temperature": Decimal(str(round(temperature, 2))),
                "humidity": Decimal(str(round(humidity, 2))),
            }
        )

        # 3. Compute moisture trend from DynamoDB history
        trend = get_moisture_trend(device_id)

        # 4. Run Decision Engine
        assessment = evaluate_plant_condition(
            soil_moisture=soil_moisture,
            temperature=temperature,
            humidity=humidity,
            moisture_trend=trend,
            min_moisture=device_cfg["min_moisture"],
            max_moisture=device_cfg["max_moisture"],
        )

        # 5. Save Assessment into DynamoDB
        assessments_table.put_item(
            Item={
                "device_id": device_id,
                "timestamp": timestamp,
                "soil_moisture": Decimal(str(round(soil_moisture, 2))),
                "temperature": Decimal(str(round(temperature, 2))),
                "humidity": Decimal(str(round(humidity, 2))),
                "moisture_trend": trend,
                "status": assessment["status"],
                "urgency": assessment["urgency"],
                "message": assessment["message"],
            }
        )

        response_payload = {
            "success": True,
            "device_id": device_id,
            "plant_name": device_cfg["plant_name"],
            "location": device_cfg["location_name"],
            "metrics": {
                "soil_moisture": soil_moisture,
                "temperature": temperature,
                "humidity": humidity,
            },
            "moisture_trend": trend,
            "status": assessment["status"],
            "urgency": assessment["urgency"],
            "message": assessment["message"],
        }

        print("Evaluation complete:", json.dumps(response_payload))

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response_payload),
        }

    except Exception as e:
        print(f"Error handling sensor payload: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"success": False, "error": str(e)}),
        }
