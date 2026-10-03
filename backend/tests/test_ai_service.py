from app.ai_context import (
    build_ai_context,
    format_ai_context
)

from app.ai_service import generate_plant_advice


# --------------------------------------------------
# Create sample GreenPulse AI context
# --------------------------------------------------

context = build_ai_context(
    plant_name="Rose",
    location_name="Kurunegala",
    soil_moisture=75.1,
    temperature=28.0,
    humidity=54.4,
    moisture_trend="INCREASING",
    moisture_change_rate=1.04,
    temperature_trend="INCREASING",
    humidity_trend="DECREASING",
    rain_expected=True,
    status="OVERWATERED",
    urgency="MEDIUM",
    decision_message=(
        "Soil moisture is very high. "
        "Avoid watering and monitor the plant."
    )
)


# --------------------------------------------------
# Convert context into readable text
# --------------------------------------------------

formatted_context = format_ai_context(context)


print("\nGreenPulse AI Input")
print("--------------------------")
print(formatted_context)


# --------------------------------------------------
# Generate AI advice
# --------------------------------------------------

print("\nGenerating AI advice...")
print("--------------------------")

advice = generate_plant_advice(formatted_context)


# --------------------------------------------------
# Display AI response
# --------------------------------------------------

print("\nGreenPulse AI Advice")
print("--------------------------")
print(advice)