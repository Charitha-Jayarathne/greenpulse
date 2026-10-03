def build_ai_context(
    plant_name,
    location_name,
    soil_moisture,
    temperature,
    humidity,
    moisture_trend,
    moisture_change_rate,
    temperature_trend,
    humidity_trend,
    rain_expected,
    status,
    urgency,
    decision_message
):
    """
    Build structured context for the AI plant-care assistant.
    """

    context = {
        "plant": {
            "name": plant_name,
            "location": location_name
        },

        "current_conditions": {
            "soil_moisture": soil_moisture,
            "temperature": temperature,
            "humidity": humidity
        },

        "historical_analysis": {
            "moisture_trend": moisture_trend,
            "moisture_change_rate": moisture_change_rate,
            "temperature_trend": temperature_trend,
            "humidity_trend": humidity_trend
        },

        "weather": {
            "rain_expected": rain_expected
        },

        "decision": {
            "status": status,
            "urgency": urgency,
            "message": decision_message
        }
    }

    return context


def format_ai_context(context):
    """
    Convert the structured AI context into readable text.
    """

    plant = context["plant"]
    current = context["current_conditions"]
    history = context["historical_analysis"]
    weather = context["weather"]
    decision = context["decision"]

    formatted_context = f"""
Plant Information:
Plant Name: {plant["name"]}
Location: {plant["location"]}

Current Sensor Conditions:
Soil Moisture: {current["soil_moisture"]}%
Temperature: {current["temperature"]}°C
Humidity: {current["humidity"]}%

Historical Analysis:
Moisture Trend: {history["moisture_trend"]}
Moisture Change Rate: {history["moisture_change_rate"]}% per reading
Temperature Trend: {history["temperature_trend"]}
Humidity Trend: {history["humidity_trend"]}

Weather:
Rain Expected: {weather["rain_expected"]}

Decision Engine Result:
Status: {decision["status"]}
Urgency: {decision["urgency"]}
Message: {decision["message"]}
"""

    return formatted_context.strip()