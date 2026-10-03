import sqlite3
from pathlib import Path


DATABASE_NAME = Path(__file__).resolve().parent.parent / "greenpulse.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # Sensor readings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            soil_moisture REAL NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL
        )
    """)

    # Devices table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            device_id TEXT PRIMARY KEY,
            plant_name TEXT NOT NULL,
            location_name TEXT NOT NULL,
            min_moisture REAL NOT NULL,
            max_moisture REAL NOT NULL
        )
    """)

    # Plant assessments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            soil_moisture REAL NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            rain_expected INTEGER NOT NULL,
            moisture_trend TEXT NOT NULL,
            status TEXT NOT NULL,
            urgency TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    # AI advice table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_advice (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            advice TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def get_device(device_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            device_id,
            plant_name,
            location_name,
            min_moisture,
            max_moisture
        FROM devices
        WHERE device_id = ?
    """, (device_id,))

    device = cursor.fetchone()

    connection.close()

    return device


def get_recent_sensor_readings(device_id, limit=10):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            timestamp,
            soil_moisture,
            temperature,
            humidity
        FROM sensor_readings
        WHERE device_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (device_id, limit))

    readings = cursor.fetchall()

    connection.close()

    return readings


def get_sensor_summary(device_id, limit=10):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            AVG(soil_moisture),
            AVG(temperature),
            AVG(humidity),
            MIN(soil_moisture),
            MAX(soil_moisture)
        FROM (
            SELECT
                soil_moisture,
                temperature,
                humidity
            FROM sensor_readings
            WHERE device_id = ?
            ORDER BY id DESC
            LIMIT ?
        )
    """, (device_id, limit))

    summary = cursor.fetchone()

    connection.close()

    return summary


def get_moisture_trend(device_id, limit=10):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT soil_moisture
        FROM sensor_readings
        WHERE device_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (device_id, limit))

    readings = cursor.fetchall()

    connection.close()

    if len(readings) < 2:
        return "INSUFFICIENT_DATA"

    newest = readings[0][0]
    oldest = readings[-1][0]

    difference = newest - oldest

    if difference > 5:
        return "INCREASING"

    if difference < -5:
        return "DECREASING"

    return "STABLE"


def get_moisture_change_rate(device_id, limit=10):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT soil_moisture
        FROM sensor_readings
        WHERE device_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (device_id, limit))

    readings = cursor.fetchall()

    connection.close()

    if len(readings) < 2:
        return 0.0

    newest = readings[0][0]
    oldest = readings[-1][0]

    change_rate = (newest - oldest) / (len(readings) - 1)

    return round(change_rate, 2)


def get_temperature_trend(device_id, limit=10):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT temperature
        FROM sensor_readings
        WHERE device_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (device_id, limit))

    readings = cursor.fetchall()

    connection.close()

    if len(readings) < 2:
        return "INSUFFICIENT_DATA"

    newest = readings[0][0]
    oldest = readings[-1][0]

    difference = newest - oldest

    if difference > 2:
        return "INCREASING"

    if difference < -2:
        return "DECREASING"

    return "STABLE"


def get_humidity_trend(device_id, limit=10):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT humidity
        FROM sensor_readings
        WHERE device_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (device_id, limit))

    readings = cursor.fetchall()

    connection.close()

    if len(readings) < 2:
        return "INSUFFICIENT_DATA"

    newest = readings[0][0]
    oldest = readings[-1][0]

    difference = newest - oldest

    if difference > 5:
        return "INCREASING"

    if difference < -5:
        return "DECREASING"

    return "STABLE"


def get_historical_analysis(device_id, limit=10):
    moisture_trend = get_moisture_trend(device_id, limit)
    moisture_change_rate = get_moisture_change_rate(device_id, limit)
    temperature_trend = get_temperature_trend(device_id, limit)
    humidity_trend = get_humidity_trend(device_id, limit)

    recent_readings = get_recent_sensor_readings(device_id, 1)
    device = get_device(device_id)

    analysis = []

    if recent_readings:
        current_moisture = recent_readings[0][1]
    else:
        current_moisture = None

    if device:
        min_moisture = device[3]
        max_moisture = device[4]
    else:
        min_moisture = None
        max_moisture = None

    # Current moisture condition
    if current_moisture is not None and min_moisture is not None:
        if current_moisture < min_moisture:
            analysis.append(
                f"Current soil moisture is below the healthy range at "
                f"{current_moisture}%. "
            )

        elif current_moisture > max_moisture:
            analysis.append(
                f"Current soil moisture is above the healthy range at "
                f"{current_moisture}%. "
            )

        else:
            analysis.append(
                f"Current soil moisture is within the healthy range at "
                f"{current_moisture}%. "
            )

    # Moisture trend
    if moisture_trend == "INCREASING":
        analysis.append(
            f"Soil moisture is increasing at "
            f"{moisture_change_rate}% per reading."
        )

    elif moisture_trend == "DECREASING":
        analysis.append(
            f"Soil moisture is decreasing at "
            f"{abs(moisture_change_rate)}% per reading."
        )

    elif moisture_trend == "STABLE":
        analysis.append(
            "Soil moisture is relatively stable."
        )

    else:
        analysis.append(
            "There is not enough moisture history for analysis."
        )

    # Temperature trend
    if temperature_trend == "INCREASING":
        analysis.append("Temperature is increasing.")

    elif temperature_trend == "DECREASING":
        analysis.append("Temperature is decreasing.")

    elif temperature_trend == "STABLE":
        analysis.append("Temperature is relatively stable.")

    # Humidity trend
    if humidity_trend == "INCREASING":
        analysis.append("Humidity is increasing.")

    elif humidity_trend == "DECREASING":
        analysis.append("Humidity is decreasing.")

    elif humidity_trend == "STABLE":
        analysis.append("Humidity is relatively stable.")

    return " ".join(analysis)


def show_sensor_readings():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            device_id,
            timestamp,
            soil_moisture,
            temperature,
            humidity
        FROM sensor_readings
        ORDER BY id DESC
    """)

    readings = cursor.fetchall()

    connection.close()

    print("\nSaved Sensor Readings")
    print("--------------------------")

    if not readings:
        print("No sensor readings found.")
        return

    for reading in readings:
        print(reading)


def show_assessments():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            device_id,
            timestamp,
            soil_moisture,
            temperature,
            humidity,
            rain_expected,
            moisture_trend,
            status,
            urgency,
            message
        FROM assessments
        ORDER BY id DESC
        LIMIT 10
    """)

    assessments = cursor.fetchall()

    connection.close()

    print("\nSaved Plant Assessments")
    print("--------------------------")

    if not assessments:
        print("No assessments found.")
        return

    for assessment in assessments:
        assessment_id = assessment[0]
        device_id = assessment[1]
        timestamp = assessment[2]
        soil_moisture = assessment[3]
        temperature = assessment[4]
        humidity = assessment[5]
        rain_expected = assessment[6]
        moisture_trend = assessment[7]
        status = assessment[8]
        urgency = assessment[9]
        message = assessment[10]

        print(f"\nAssessment ID: {assessment_id}")
        print(f"Device ID: {device_id}")
        print(f"Timestamp: {timestamp}")
        print(f"Soil Moisture: {soil_moisture}%")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Rain Expected: {bool(rain_expected)}")
        print(f"Moisture Trend: {moisture_trend}")
        print(f"Status: {status}")
        print(f"Urgency: {urgency}")
        print(f"Message: {message}")

def save_ai_advice(device_id, timestamp, advice):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO ai_advice (
            device_id,
            timestamp,
            advice
        )
        VALUES (?, ?, ?)
    """, (
        device_id,
        timestamp,
        advice
    ))

    connection.commit()
    connection.close()

if __name__ == "__main__":

    create_tables()

    device = get_device("greenpulse-001")

    if device:
        print("\nDevice Configuration")
        print("--------------------------")
        print(f"Device ID: {device[0]}")
        print(f"Plant Name: {device[1]}")
        print(f"Location: {device[2]}")
        print(f"Minimum Moisture: {device[3]}%")
        print(f"Maximum Moisture: {device[4]}%")
    else:
        print("Device not found.")

    show_sensor_readings()

    show_assessments()