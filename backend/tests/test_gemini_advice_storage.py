from datetime import datetime

from app.ai_service import generate_plant_advice
from app.database import create_tables, save_ai_advice, get_connection


print("\nGreenPulse Gemini AI Advice Storage Test")
print("----------------------------------------")


# --------------------------------------------------
# Make sure database tables exist
# --------------------------------------------------

create_tables()


# --------------------------------------------------
# Prepare test AI context
# --------------------------------------------------

ai_context = """
Plant Information:
Plant Name: Rose
Location: Kurunegala

Current Sensor Conditions:
Soil Moisture: 45.5%
Temperature: 27.2°C
Humidity: 65.0%

Historical Analysis:
Moisture Trend: INCREASING
Moisture Change Rate: 1.0% per reading
Temperature Trend: INCREASING
Humidity Trend: INCREASING

Weather:
Rain Expected: True

Decision Engine Result:
Status: HEALTHY
Urgency: LOW
Message: Current plant conditions are within the normal range.
"""


# --------------------------------------------------
# Generate real Gemini advice
# --------------------------------------------------

print("\nGenerating Gemini advice...")
print("----------------------------------------")

try:

    advice = generate_plant_advice(
        ai_context
    )

    print("\nGemini Advice:")
    print("----------------------------------------")
    print(advice)


    # --------------------------------------------------
    # Save real Gemini advice to database
    # --------------------------------------------------

    timestamp = datetime.utcnow().isoformat() + "Z"

    save_ai_advice(
        device_id="greenpulse-001",
        timestamp=timestamp,
        advice=advice
    )

    print("\nAI advice saved successfully to database.")


    # --------------------------------------------------
    # Read latest AI advice from database
    # --------------------------------------------------

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            device_id,
            timestamp,
            advice
        FROM ai_advice
        ORDER BY id DESC
        LIMIT 1
    """)

    record = cursor.fetchone()

    connection.close()


    # --------------------------------------------------
    # Display saved record
    # --------------------------------------------------

    print("\nLatest AI Advice Database Record")
    print("----------------------------------------")

    if record:

        print(f"ID: {record[0]}")
        print(f"Device ID: {record[1]}")
        print(f"Timestamp: {record[2]}")
        print(f"Advice: {record[3]}")

    else:

        print("No AI advice record found.")


    print("\nGemini AI advice storage test completed.")


except Exception as error:

    print("\nGemini AI advice generation failed.")
    print(error)