import json

import paho.mqtt.client as mqtt

from database import (
    get_connection,
    get_device,
    get_sensor_summary,
    get_moisture_trend,
    get_moisture_change_rate,
    get_temperature_trend,
    get_humidity_trend,
    get_historical_analysis,
    save_ai_advice
)

from weather import is_rain_expected
from decision_engine import evaluate_plant_condition

from ai_context import (
    build_ai_context,
    format_ai_context
)

from ai_service import generate_plant_advice

from ai_scheduler import (
    can_generate_ai_advice,
    record_ai_request
)


# --------------------------------------------------
# MQTT Configuration
# --------------------------------------------------

MQTT_BROKER = "localhost"

MQTT_PORT = 1883

MQTT_TOPIC = "greenpulse/sensor/data"

MQTT_AI_QUOTE_TOPIC = "greenpulse/ai/quote"

MQTT_PLANT_STATUS_TOPIC = "greenpulse/plant/status"


# --------------------------------------------------
# MQTT Connection
# --------------------------------------------------

def on_connect(client, userdata, flags, reason_code, properties):

    print(f"Connected to MQTT broker with result code: {reason_code}")

    client.subscribe(MQTT_TOPIC)

    print(f"Subscribed to: {MQTT_TOPIC}")


# --------------------------------------------------
# MQTT Message Processing
# --------------------------------------------------

def on_message(client, userdata, message):

    payload = message.payload.decode("utf-8")

    print("\nReceived message:")
    print(payload)

    try:

        # --------------------------------------------------
        # Convert JSON payload into Python data
        # --------------------------------------------------

        sensor_data = json.loads(payload)

        device_id = sensor_data["device_id"]
        timestamp = sensor_data["timestamp"]

        soil_moisture = sensor_data["soil_moisture"]
        temperature = sensor_data["temperature"]
        humidity = sensor_data["humidity"]


        # --------------------------------------------------
        # Validate sensor values
        # --------------------------------------------------

        if not 0 <= soil_moisture <= 100:

            print("Invalid soil moisture value.")

            return


        if not 0 <= humidity <= 100:

            print("Invalid humidity value.")

            return


        if not -40 <= temperature <= 80:

            print("Invalid temperature value.")

            return


        print(f"Soil Moisture: {soil_moisture}%")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")


        # --------------------------------------------------
        # Get device configuration
        # --------------------------------------------------

        device = get_device(device_id)

        if device is None:

            print(
                f"Device configuration not found: "
                f"{device_id}"
            )

            return


        plant_name = device[1]
        location_name = device[2]

        min_moisture = device[3]
        max_moisture = device[4]


        print(f"Plant: {plant_name}")
        print(f"Location: {location_name}")

        print(
            f"Moisture Range: "
            f"{min_moisture}% - {max_moisture}%"
        )


        # --------------------------------------------------
        # Save current sensor reading FIRST
        # --------------------------------------------------

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO sensor_readings (
                device_id,
                timestamp,
                soil_moisture,
                temperature,
                humidity
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            device_id,
            timestamp,
            soil_moisture,
            temperature,
            humidity
        ))

        connection.commit()
        connection.close()


        # --------------------------------------------------
        # Get recent historical sensor data
        # --------------------------------------------------

        summary = get_sensor_summary(device_id)

        moisture_trend = get_moisture_trend(device_id)

        moisture_change_rate = get_moisture_change_rate(
            device_id
        )

        temperature_trend = get_temperature_trend(
            device_id
        )

        humidity_trend = get_humidity_trend(
            device_id
        )

        historical_analysis = get_historical_analysis(
            device_id
        )


        # --------------------------------------------------
        # Display historical sensor information
        # --------------------------------------------------

        if summary:

            (
                average_soil_moisture,
                average_temperature,
                average_humidity,
                minimum_soil_moisture,
                maximum_soil_moisture
            ) = summary


            print("\nRecent Sensor History")
            print("--------------------------")


            print(
                f"Average Soil Moisture: "
                f"{average_soil_moisture:.2f}%"
            )


            print(
                f"Average Temperature: "
                f"{average_temperature:.2f}°C"
            )


            print(
                f"Average Humidity: "
                f"{average_humidity:.2f}%"
            )


            print(
                f"Minimum Soil Moisture: "
                f"{minimum_soil_moisture:.2f}%"
            )


            print(
                f"Maximum Soil Moisture: "
                f"{maximum_soil_moisture:.2f}%"
            )


            print(
                f"Moisture Trend: "
                f"{moisture_trend}"
            )


            print(
                f"Moisture Change Rate: "
                f"{moisture_change_rate}% per reading"
            )


            print(
                f"Temperature Trend: "
                f"{temperature_trend}"
            )


            print(
                f"Humidity Trend: "
                f"{humidity_trend}"
            )


            print(
                f"Historical Analysis: "
                f"{historical_analysis}"
            )


        # --------------------------------------------------
        # Get weather information
        # --------------------------------------------------

        rain_expected = is_rain_expected(
            location_name
        )


        # --------------------------------------------------
        # Evaluate plant condition
        # --------------------------------------------------

        result = evaluate_plant_condition(

            soil_moisture=soil_moisture,

            temperature=temperature,

            humidity=humidity,

            rain_expected=rain_expected,

            moisture_trend=moisture_trend,

            min_moisture=min_moisture,

            max_moisture=max_moisture
        )


        # --------------------------------------------------
        # Display GreenPulse decision
        # --------------------------------------------------

        print("\nGreenPulse Plant Assessment")
        print("--------------------------")

        print(
            f"Rain Expected: "
            f"{rain_expected}"
        )

        print(
            f"Status: "
            f"{result['status']}"
        )

        print(
            f"Urgency: "
            f"{result['urgency']}"
        )

        print(
            f"Message: "
            f"{result['message']}"
        )


        # --------------------------------------------------
        # Publish Plant Status to MQTT
        # --------------------------------------------------

        plant_status = {
            "device_id": device_id,
            "plant_name": plant_name,
            "location": location_name,
            "status": result["status"],
            "urgency": result["urgency"],
            "message": result["message"]
        }


        publish_result = client.publish(
            MQTT_PLANT_STATUS_TOPIC,
            json.dumps(plant_status)
        )


        if publish_result.rc == mqtt.MQTT_ERR_SUCCESS:

            print(
                f"Plant status published successfully to: "
                f"{MQTT_PLANT_STATUS_TOPIC}"
            )

        else:

            print(
                f"Failed to publish plant status to: "
                f"{MQTT_PLANT_STATUS_TOPIC}"
            )


        # --------------------------------------------------
        # Build AI Context
        # --------------------------------------------------

        ai_context = build_ai_context(

            plant_name=plant_name,

            location_name=location_name,

            soil_moisture=soil_moisture,

            temperature=temperature,

            humidity=humidity,

            moisture_trend=moisture_trend,

            moisture_change_rate=moisture_change_rate,

            temperature_trend=temperature_trend,

            humidity_trend=humidity_trend,

            rain_expected=rain_expected,

            status=result["status"],

            urgency=result["urgency"],

            decision_message=result["message"]
        )


        # --------------------------------------------------
        # Format AI Context
        # --------------------------------------------------

        formatted_ai_context = format_ai_context(
            ai_context
        )


        print("\nGreenPulse AI Context")
        print("--------------------------")

        print(formatted_ai_context)


        # --------------------------------------------------
        # AI Generation Status
        # --------------------------------------------------

        ai_generated = False


        # --------------------------------------------------
        # Check AI Schedule
        # --------------------------------------------------

        if can_generate_ai_advice():

            print("\nAI advice window is active.")
            print("Generating AI advice...")
            print("--------------------------")


            try:

                # --------------------------------------------------
                # Generate AI Plant-Care Advice
                # --------------------------------------------------

                ai_advice = generate_plant_advice(
                    formatted_ai_context
                )


                # --------------------------------------------------
                # Save AI Advice to Database
                # --------------------------------------------------

                save_ai_advice(
                    device_id=device_id,
                    timestamp=timestamp,
                    advice=ai_advice
                )


                print(
                    "AI advice saved successfully to database."
                )


                # --------------------------------------------------
                # Publish AI Advice to MQTT
                # --------------------------------------------------

                publish_result = client.publish(
                    MQTT_AI_QUOTE_TOPIC,
                    ai_advice
                )


                if publish_result.rc == mqtt.MQTT_ERR_SUCCESS:

                    print(
                        f"AI advice published successfully to: "
                        f"{MQTT_AI_QUOTE_TOPIC}"
                    )

                else:

                    print(
                        f"Failed to publish AI advice to: "
                        f"{MQTT_AI_QUOTE_TOPIC}"
                    )


                # --------------------------------------------------
                # Record successful AI request
                # --------------------------------------------------

                record_ai_request()


                # --------------------------------------------------
                # Display AI Advice
                # --------------------------------------------------

                print("\nGreenPulse AI Advice")
                print("--------------------------")

                print(ai_advice)


                ai_generated = True


            except Exception as ai_error:

                print(
                    "\nAI advice generation failed:"
                )

                print(ai_error)

                ai_generated = False


        else:

            print("\nAI advice window is not active.")
            print("Gemini request skipped.")

            ai_generated = False


        # --------------------------------------------------
        # Save Plant Assessment
        # --------------------------------------------------

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO assessments (
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
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            device_id,
            timestamp,
            soil_moisture,
            temperature,
            humidity,
            int(rain_expected),
            moisture_trend,
            result["status"],
            result["urgency"],
            result["message"]
        ))

        connection.commit()
        connection.close()


        # --------------------------------------------------
        # Processing Completed
        # --------------------------------------------------

        print("\nGreenPulse Processing Completed")
        print("--------------------------")

        print("Sensor data saved to database.")

        print("Plant assessment saved to database.")


        if ai_generated:

            print(
                "AI plant-care advice generated "
                "and saved successfully."
            )

        else:

            print(
                "AI plant-care advice was not generated "
                "for this sensor reading."
            )


    # --------------------------------------------------
    # Handle Invalid JSON
    # --------------------------------------------------

    except json.JSONDecodeError:

        print("Invalid JSON received.")


    # --------------------------------------------------
    # Handle Missing Sensor Fields
    # --------------------------------------------------

    except KeyError as error:

        print(
            f"Missing sensor field: "
            f"{error}"
        )


    # --------------------------------------------------
    # Handle Other Errors
    # --------------------------------------------------

    except Exception as error:

        print(
            f"Error processing sensor data: "
            f"{error}"
        )


# --------------------------------------------------
# MQTT Client Setup
# --------------------------------------------------

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)


client.on_connect = on_connect

client.on_message = on_message


# --------------------------------------------------
# Connect to MQTT Broker
# --------------------------------------------------

client.connect(
    MQTT_BROKER,
    MQTT_PORT,
    60
)


print(
    "GreenPulse MQTT receiver started..."
)


# --------------------------------------------------
# Start MQTT Network Loop
# --------------------------------------------------

client.loop_forever()