"""
GreenPulse Plant Registry Service
Manages plant profiles, device switching, and moisture threshold configuration.
Saves to DynamoDB 'greenpulse_devices'.
"""

import os
from decimal import Decimal
from pathlib import Path
import boto3
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
devices_table = dynamodb.Table("greenpulse_devices")

# Popular plant presets with recommended moisture limits
PLANT_PRESETS = {
    "Rose": {"min_moisture": 30.0, "max_moisture": 70.0, "notes": "Moderate moisture, thrives in sunlight"},
    "Tomato": {"min_moisture": 50.0, "max_moisture": 75.0, "notes": "High moisture requirement, regular watering needed"},
    "Cactus": {"min_moisture": 10.0, "max_moisture": 30.0, "notes": "Drought tolerant, low water needs"},
    "Succulent": {"min_moisture": 15.0, "max_moisture": 35.0, "notes": "Allow soil to dry out between waterings"},
    "Fern": {"min_moisture": 60.0, "max_moisture": 80.0, "notes": "High humidity and consistently damp soil"},
    "Mint": {"min_moisture": 55.0, "max_moisture": 75.0, "notes": "Loves moist soil, fast growing"},
    "Monstera": {"min_moisture": 35.0, "max_moisture": 65.0, "notes": "Allow top 2 inches to dry before watering"},
    "Chili / Pepper": {"min_moisture": 45.0, "max_moisture": 70.0, "notes": "Warm conditions, steady moisture"},
    "Orchid": {"min_moisture": 25.0, "max_moisture": 50.0, "notes": "Epiphytic, needs well-draining medium"}
}


def register_plant(device_id, plant_name, location_name="Balcony", min_moisture=None, max_moisture=None, scientific_name=None, category=None, sunlight=None, notes=None):
    """
    Registers or updates the active plant for a given device in DynamoDB.
    Supports autonomous AI moisture calibration and botanical metadata.
    """
    # Fallback to defaults if min/max moisture omitted
    if min_moisture is None or max_moisture is None:
        preset = PLANT_PRESETS.get(plant_name, {"min_moisture": 30.0, "max_moisture": 70.0})
        min_moisture = min_moisture if min_moisture is not None else preset.get("min_moisture", 30.0)
        max_moisture = max_moisture if max_moisture is not None else preset.get("max_moisture", 70.0)

    item = {
        "device_id": str(device_id),
        "plant_name": str(plant_name),
        "location_name": str(location_name),
        "min_moisture": Decimal(str(round(float(min_moisture), 1))),
        "max_moisture": Decimal(str(round(float(max_moisture), 1))),
        "scientific_name": str(scientific_name or ""),
        "category": str(category or "Botanical Specimen"),
        "sunlight": str(sunlight or "Indirect Sunlight"),
        "notes": str(notes or "Auto-calibrated by Gemini AI")
    }

    try:
        devices_table.put_item(Item=item)
        print(f"[REGISTRY] Successfully registered device '{device_id}' to plant '{plant_name}' ({min_moisture}% - {max_moisture}%) in DynamoDB")
        return {
            "success": True,
            "device_id": device_id,
            "plant_name": plant_name,
            "scientific_name": scientific_name,
            "location": location_name,
            "min_moisture": float(min_moisture),
            "max_moisture": float(max_moisture)
        }
    except Exception as e:
        print(f"[REGISTRY] Failed to register device in DynamoDB: {e}")
        return {"success": False, "error": str(e)}


def get_plant_config(device_id="greenpulse-001"):
    """Fetch the active plant configuration for a device."""
    try:
        response = devices_table.get_item(Key={"device_id": str(device_id)})
        item = response.get("Item")
        if item:
            return {
                "device_id": item["device_id"],
                "plant_name": item["plant_name"],
                "location_name": item["location_name"],
                "min_moisture": float(item["min_moisture"]),
                "max_moisture": float(item["max_moisture"])
            }
    except Exception as e:
        print(f"[REGISTRY] Error retrieving device config: {e}")

    # Fallback default
    return {
        "device_id": device_id,
        "plant_name": "Rose",
        "location_name": "Kurunegala",
        "min_moisture": 30.0,
        "max_moisture": 70.0
    }


if __name__ == "__main__":
    # Test registering a Tomato plant for device greenpulse-001
    res = register_plant("greenpulse-001", "Tomato", "Kitchen Garden", 50.0, 75.0)
    print("Registration Result:", res)
    active = get_plant_config("greenpulse-001")
    print("Active Config:", active)
