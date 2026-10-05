try:
    from app.weather import is_rain_expected
except ImportError:
    from weather import is_rain_expected

def evaluate_plant_condition(
    soil_moisture,
    temperature,
    humidity,
    rain_expected=False,
    moisture_trend="STABLE",
    min_moisture=30,
    max_moisture=70
):
    """
    Evaluate the current plant condition using sensor
    readings, historical moisture trend, and weather information.
    """

    # Very dry soil
    if soil_moisture < min_moisture:

        # Soil is recovering and rain is expected
        if rain_expected and moisture_trend == "INCREASING":
            return {
                "status": "MONITOR",
                "urgency": "LOW",
                "message": "Soil moisture is low but increasing, and rain is expected."
            }

        # Soil is dry but rain is expected
        if rain_expected:
            return {
                "status": "MONITOR",
                "urgency": "MEDIUM",
                "message": "Soil moisture is low, but rain is expected."
            }

        # Soil is dry and no rain is expected
        return {
            "status": "WATER_NEEDED",
            "urgency": "HIGH",
            "message": "Soil moisture is low and watering may be required."
        }

    # Hot conditions combined with moderately dry soil
    if temperature >= 33 and soil_moisture < 45:
        return {
            "status": "URGENT_CARE",
            "urgency": "HIGH",
            "message": "High temperature and low soil moisture detected."
        }

    # Very wet soil
    if soil_moisture > max_moisture:
        return {
            "status": "OVERWATERED",
            "urgency": "MEDIUM",
            "message": "Soil moisture is very high. Avoid watering and monitor the plant."
        }

    # Healthy conditions
    if min_moisture <= soil_moisture <= max_moisture and temperature < 33:
        return {
            "status": "HEALTHY",
            "urgency": "LOW",
            "message": "Current plant conditions are within the normal range."
        }

    # Default condition
    return {
        "status": "MONITOR",
        "urgency": "MEDIUM",
        "message": "Plant conditions should be monitored."
    }


if __name__ == "__main__":

    test_cases = [
        {
            "name": "Dry soil, no rain",
            "soil_moisture": 20,
            "temperature": 28,
            "humidity": 60,
            "rain_expected": False,
            "moisture_trend": "DECREASING"
        },
        {
            "name": "Dry soil, rain expected",
            "soil_moisture": 20,
            "temperature": 28,
            "humidity": 60,
            "rain_expected": True,
            "moisture_trend": "STABLE"
        },
        {
            "name": "Dry soil, increasing moisture, rain expected",
            "soil_moisture": 20,
            "temperature": 28,
            "humidity": 60,
            "rain_expected": True,
            "moisture_trend": "INCREASING"
        },
        {
            "name": "Hot and dry",
            "soil_moisture": 35,
            "temperature": 35,
            "humidity": 45,
            "rain_expected": False,
            "moisture_trend": "DECREASING"
        },
        {
            "name": "Healthy plant",
            "soil_moisture": 50,
            "temperature": 27,
            "humidity": 65,
            "rain_expected": False,
            "moisture_trend": "STABLE"
        },
        {
            "name": "Very wet soil",
            "soil_moisture": 80,
            "temperature": 26,
            "humidity": 75,
            "rain_expected": False,
            "moisture_trend": "INCREASING"
        }
    ]

    for test in test_cases:

        result = evaluate_plant_condition(
            soil_moisture=test["soil_moisture"],
            temperature=test["temperature"],
            humidity=test["humidity"],
            rain_expected=test["rain_expected"],
            moisture_trend=test["moisture_trend"]
        )

        print("\nTest:", test["name"])
        print("--------------------------")
        print(f"Soil Moisture: {test['soil_moisture']}%")
        print(f"Temperature: {test['temperature']}°C")
        print(f"Humidity: {test['humidity']}%")
        print(f"Rain Expected: {test['rain_expected']}")
        print(f"Moisture Trend: {test['moisture_trend']}")
        print(f"Status: {result['status']}")
        print(f"Urgency: {result['urgency']}")
        print(f"Message: {result['message']}")

    print("\nPlant-Specific Test")
    print("--------------------------")

    result = evaluate_plant_condition(
        soil_moisture=25,
        temperature=27,
        humidity=65,
        rain_expected=False,
        moisture_trend="DECREASING",
        min_moisture=20,
        max_moisture=50
    )

    print("Plant: Example Plant")
    print("Moisture Range: 20% - 50%")
   