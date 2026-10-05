"""
GreenPulse Backend API Server
Provides endpoints for:
- Live Weather & Rain Forecast (OpenWeather API)
- Plant Profile & Configuration (with preset library and DynamoDB sync)
- Gemini AI Botanical Diagnosis (combines Sensor Telemetry + Plant Profile + Live Weather + Decision Engine)
Runs on port 5005.
"""

import os
import sys
from decimal import Decimal
from pathlib import Path
from flask import Flask, request, jsonify

# Ensure backend directory is in python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "app"))

from dotenv import load_dotenv
load_dotenv(BASE_DIR / ".env")

from app.weather import get_current_weather, is_rain_expected
from app.decision_engine import evaluate_plant_condition
from app.ai_service import generate_plant_advice
from app.plant_registry import PLANT_PRESETS, register_plant, get_plant_config

app = Flask(__name__)

# Add CORS headers to all responses
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
    return response

# In-memory cached active plant & city config
active_config = {
    "device_id": "greenpulse-team-infinix",
    "plant_name": "Tomato",
    "location_name": "Colombo",
    "min_moisture": 50.0,
    "max_moisture": 75.0,
    "notes": "High moisture requirement, regular watering needed"
}

# Cache for latest sensor telemetry
latest_sensor_data = {
    "device_id": "greenpulse-team-infinix",
    "temperature": 25.2,
    "humidity": 49.0,
    "soil_moisture": 66.0,
    "soil_temperature": 23.8,
    "air_quality_percent": 100.0,
    "air_pressure": 1012.1,
    "timestamp": "2026-10-06T00:54:00Z"
}

# Cache for latest weather
cached_weather = {
    "city": "Colombo",
    "temp": 27.0,
    "humidity": 85,
    "description": "Scattered Clouds",
    "rain_expected": True,
    "last_fetched": 0
}

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "GreenPulse AI & Weather Backend"})

@app.route("/api/config", methods=["GET"])
def get_config():
    return jsonify({
        "config": active_config,
        "presets": PLANT_PRESETS
    })

@app.route("/api/config", methods=["POST"])
def update_config():
    data = request.get_json() or {}
    plant_name = data.get("plant_name", active_config["plant_name"])
    location_name = data.get("location_name", active_config["location_name"])
    
    preset = PLANT_PRESETS.get(plant_name, {})
    min_m = float(data.get("min_moisture", preset.get("min_moisture", 30.0)))
    max_m = float(data.get("max_moisture", preset.get("max_moisture", 70.0)))
    notes = preset.get("notes", "Custom botanical threshold")

    active_config["plant_name"] = plant_name
    active_config["location_name"] = location_name
    active_config["min_moisture"] = min_m
    active_config["max_moisture"] = max_m
    active_config["notes"] = notes

    # Try to register in DynamoDB in background
    try:
        register_plant(
            device_id=active_config["device_id"],
            plant_name=plant_name,
            location_name=location_name,
            min_moisture=min_m,
            max_moisture=max_m
        )
    except Exception as e:
        print(f"Warning: DynamoDB registration error (using local state): {e}")

    # Immediately fetch fresh weather for the new location
    weather_info = fetch_weather(location_name)

    return jsonify({
        "success": True,
        "message": f"Updated active plant to {plant_name} in {location_name}",
        "config": active_config,
        "weather": weather_info
    })

def fetch_weather(city_name):
    try:
        cw = get_current_weather(city_name)
        rain = is_rain_expected(city_name)
        cached_weather["city"] = city_name
        cached_weather["temp"] = round(cw["main"]["temp"], 1)
        cached_weather["humidity"] = cw["main"]["humidity"]
        cached_weather["description"] = cw["weather"][0]["description"].title()
        cached_weather["rain_expected"] = rain
        return cached_weather
    except Exception as e:
        print(f"Weather fetch error for {city_name}: {e}")
        cached_weather["city"] = city_name
        cached_weather["description"] = "Weather API Offline"
        return cached_weather

@app.route("/api/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city", active_config["location_name"])
    return jsonify(fetch_weather(city))

@app.route("/api/sensor/latest", methods=["GET", "POST"])
def sensor_endpoint():
    if request.method == "POST":
        data = request.get_json() or {}
        latest_sensor_data.update(data)
        return jsonify({"status": "received", "data": latest_sensor_data})
    return jsonify(latest_sensor_data)

@app.route("/api/ai/diagnose", methods=["POST"])
def ai_diagnose():
    req_data = request.get_json() or {}
    
    # Allow caller to override or pass live sensor values
    sensor = {**latest_sensor_data, **req_data.get("sensor", {})}
    plant = req_data.get("plant", active_config)
    city = plant.get("location_name", active_config["location_name"])
    
    weather_info = fetch_weather(city)
    rain = weather_info.get("rain_expected", False)
    
    # Run Decision Engine evaluation
    try:
        eval_result = evaluate_plant_condition(
            soil_moisture=float(sensor.get("soil_moisture", 50)),
            temperature=float(sensor.get("temperature", 25)),
            humidity=float(sensor.get("humidity", 50)),
            rain_expected=rain,
            min_moisture=float(plant.get("min_moisture", 30)),
            max_moisture=float(plant.get("max_moisture", 70))
        )
    except Exception as e:
        print(f"Decision engine error: {e}")
        eval_result = {"status": "NORMAL", "urgency": "LOW", "message": "Optimal plant condition"}

    # Formulate rich botanical prompt context
    context = f"""
Plant Species: {plant.get('plant_name', 'Houseplant')}
Location: {city}
Target Soil Moisture Range: {plant.get('min_moisture', 30)}% - {plant.get('max_moisture', 70)}%

Physical ESP32 Sensor Telemetry:
- Soil Moisture: {sensor.get('soil_moisture')}%
- Soil Temperature (Root Zone): {sensor.get('soil_temperature')} °C
- Ambient Air Temperature: {sensor.get('temperature')} °C
- Relative Air Humidity: {sensor.get('humidity')} %
- Air Quality Index: {sensor.get('air_quality_percent')} %
- Barometric Pressure: {sensor.get('air_pressure')} hPa

Live City Weather Forecast ({city}):
- Outside Temperature: {weather_info.get('temp')} °C
- Outside Humidity: {weather_info.get('humidity')} %
- Weather Condition: {weather_info.get('description')}
- Rain Expected in Next 24 Hours: {'YES (Precipitation Likely)' if rain else 'NO (Clear/Dry)'}

Decision Engine Pre-Assessment:
- Health Status: {eval_result.get('status')}
- Urgency Level: {eval_result.get('urgency')}
- Primary Alert: {eval_result.get('message')}
"""

    try:
        advice_text = generate_plant_advice(context)
    except Exception as e:
        print(f"Gemini API error: {e}")
        advice_text = f"Health Status: {eval_result.get('status')} ({eval_result.get('message')}). Recommendation: Maintain current care routine."

    return jsonify({
        "success": True,
        "evaluation": eval_result,
        "weather": weather_info,
        "plant": plant,
        "sensor": sensor,
        "advice": advice_text
    })

if __name__ == "__main__":
    print("=" * 60)
    print("GreenPulse AI & Weather Backend Server")
    print("Port: 5005")
    print("Endpoints: /api/config, /api/weather, /api/ai/diagnose")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5005, debug=False)
