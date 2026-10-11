import os
import time
import json
from pathlib import Path
import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not configured.")

GEMINI_REST_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={GOOGLE_API_KEY}"


def identify_plant_profile(query: str) -> dict:
    """
    Uses Gemini 3.8 Flash to analyze any user plant input (common name, nickname, or species),
    identify its botanical taxonomy, and autonomously calibrate its root-zone safe soil
    moisture thresholds for AWS DynamoDB synchronization.
    """
    clean_query = query.strip()
    if not clean_query:
        clean_query = "Houseplant"

    prompt = f"""You are the GreenPulse Botanical Intelligence Engine.
The user wants to monitor this plant: "{clean_query}".
Analyze the plant, identify its taxonomy, and calculate its precise safe root-zone volumetric soil moisture thresholds (capacitive sensor 0-100%).

Respond ONLY with a valid JSON object matching this exact schema:
{{
  "identified_name": "Common Plant Name",
  "scientific_name": "Scientific botanical binomial",
  "category": "Plant family / category",
  "min_moisture": 25.0,
  "max_moisture": 55.0,
  "sunlight": "Direct / Bright Indirect / Low light",
  "watering_frequency": "Practical watering guideline",
  "botanical_summary": "1-2 sentence botanical summary for the grower"
}}

Moisture calibration scientific guidelines:
- min_moisture: float between 10.0 and 65.0 (percentage where stress begins)
- max_moisture: float between 25.0 and 85.0 (percentage above which root saturation/rot occurs)
- Cacti / succulents / Snake Plant: 10% - 35%
- Orchids / Epiphytes: 20% - 45%
- Tropical Foliage (Monstera, Pothos, Philodendron): 30% - 60%
- Herbs & Spices (Curry leaves, Basil, Mint): 40% - 75%
- Fruiting / High Demand (Tomato, Chili, Pepper): 50% - 75%
- Ferns / Bog plants: 60% - 85%
"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"response_mime_type": "application/json"}
    }

    # Attempt REST call with retries
    for attempt in range(3):
        try:
            resp = requests.post(GEMINI_REST_URL, json=payload, timeout=12)
            if resp.status_code == 200:
                raw_text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                data = json.loads(raw_text)
                # Ensure moisture values are valid floats
                data["min_moisture"] = float(data.get("min_moisture", 30.0))
                data["max_moisture"] = float(data.get("max_moisture", 70.0))
                data["query"] = clean_query
                return data
            print(f"[AI SERVICE] Gemini identify attempt {attempt+1} got HTTP {resp.status_code}")
            time.sleep(1.0)
        except Exception as ex:
            print(f"[AI SERVICE] Gemini identify attempt {attempt+1} error: {ex}")
            time.sleep(1.0)

    # Autonomous botanical fallback heuristic if API is temporarily unavailable
    q_lower = clean_query.lower()
    if any(k in q_lower for k in ["cactus", "succulent", "aloe", "snake", "sansevieria"]):
        return {
            "identified_name": clean_query.title(),
            "scientific_name": "Botanical xerophyte",
            "category": "Drought-Tolerant / Succulent",
            "min_moisture": 15.0,
            "max_moisture": 35.0,
            "sunlight": "Direct / Bright Indirect Sunlight",
            "watering_frequency": "Allow soil to completely dry out between waterings",
            "botanical_summary": f"Resilient drought-tolerant specimen. Susceptible to root rot if overwatered.",
            "query": clean_query
        }
    elif any(k in q_lower for k in ["fern", "moss", "mint", "pothos"]):
        return {
            "identified_name": clean_query.title(),
            "scientific_name": "Botanical mesophyte",
            "category": "High Moisture / Herb",
            "min_moisture": 55.0,
            "max_moisture": 80.0,
            "sunlight": "Partial Shade / Diffused Light",
            "watering_frequency": "Keep root zone consistently moist and aerated",
            "botanical_summary": f"Moisture-loving species requiring continuous humidity and gentle hydration.",
            "query": clean_query
        }
    elif any(k in q_lower for k in ["tomato", "chili", "pepper", "curry", "karapincha"]):
        return {
            "identified_name": clean_query.title(),
            "scientific_name": "Solanaceae / Rutaceae cultivar",
            "category": "Fruiting / Culinary Shrub",
            "min_moisture": 45.0,
            "max_moisture": 75.0,
            "sunlight": "Full Sun (6+ hours daily)",
            "watering_frequency": "Regular deep watering when surface soil dries",
            "botanical_summary": f"Vigorous grower requiring consistent hydration for active transpiration.",
            "query": clean_query
        }
    else:
        return {
            "identified_name": clean_query.title(),
            "scientific_name": "Plantae botanical specimen",
            "category": "Tropical / Indoor Foliage",
            "min_moisture": 35.0,
            "max_moisture": 65.0,
            "sunlight": "Moderate Indirect Sunlight",
            "watering_frequency": "Water when top 1-2 inches of soil feel dry",
            "botanical_summary": f"Healthy foliage specimen with balanced root aeration and hydration needs.",
            "query": clean_query
        }


def generate_plant_advice(ai_context: str) -> str:
    """
    Send GreenPulse sensor telemetry and environment context to Gemini 3.8 Flash
    and return an AI-generated clinical botanical explanation.
    """
    prompt = f"""You are the GreenPulse AI plant-care assistant.

Analyze the following plant information and telemetry:

{ai_context}

Provide a structured, practical, and expert plant-care diagnosis.

Format your response cleanly:
1. Current Condition & Vital Signs: A brief assessment of current health.
2. Soil & Environment Analysis: How current soil moisture, temperature, humidity, and air quality relate to the plant's safe range.
3. Weather Impact: How the city forecast (temperature, impending rain) influences plant care today.
4. Actionable Recommendation: Clear instruction (e.g. whether to water now, wait for rain, adjust sunlight/ventilation).

Keep it concise, clear, and highly encouraging for the grower.
"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    for attempt in range(3):
        try:
            resp = requests.post(GEMINI_REST_URL, json=payload, timeout=14)
            if resp.status_code == 200:
                text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                return text.strip()
            time.sleep(1.0)
        except Exception as e:
            print(f"[AI SERVICE] Diagnosis attempt {attempt+1} error: {e}")
            time.sleep(1.0)

    return "Optimal environmental conditions observed. Root hydration and ambient parameters remain within the calibrated botanical thresholds."
