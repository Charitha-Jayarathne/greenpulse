from app.database import create_tables, save_ai_advice, get_connection


print("\nGreenPulse AI Advice Storage Test")
print("--------------------------")


# Make sure all database tables exist
create_tables()


# Test AI advice
device_id = "greenpulse-001"
timestamp = "2026-10-03T08:00:00Z"
advice = (
    "The plant is currently in a healthy condition. "
    "Continue monitoring soil moisture and avoid unnecessary watering."
)


# Save the AI advice
save_ai_advice(
    device_id,
    timestamp,
    advice
)

print("\nAI advice saved successfully.")


# Read the latest saved AI advice
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


# Display the saved record
print("\nLatest AI Advice Record")
print("--------------------------")

if record:
    print(f"ID: {record[0]}")
    print(f"Device ID: {record[1]}")
    print(f"Timestamp: {record[2]}")
    print(f"Advice: {record[3]}")
else:
    print("No AI advice record found.")


print("\nAI advice storage test completed.")