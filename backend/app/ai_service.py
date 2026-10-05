import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not configured.")

client = genai.Client(api_key=GOOGLE_API_KEY)

def generate_plant_advice(ai_context):
    """
    Send GreenPulse plant information to Gemini
    and return an AI-generated care explanation.
    """
    prompt = f"""
You are the GreenPulse AI plant-care assistant.

Analyze the following plant information.

{ai_context}

Provide a structured, practical, and expert plant-care diagnosis.

Format your response cleanly:
1. Current Condition & Vital Signs: A brief assessment of current health.
2. Soil & Environment Analysis: How current soil moisture, temperature, humidity, and air quality relate to the plant's safe range.
3. Weather Impact: How the city forecast (temperature, impending rain) influences plant care today.
4. Actionable Recommendation: Clear instruction (e.g. whether to water now, wait for rain, adjust sunlight/ventilation).

Keep it concise, clear, and highly encouraging for the grower.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text.strip() if response.text else "Healthy conditions detected."
