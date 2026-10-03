import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# --------------------------------------------------
# Gemini API configuration
# --------------------------------------------------

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not configured.")


# --------------------------------------------------
# Create Gemini LLM
# --------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0.2,
    google_api_key=GOOGLE_API_KEY
)


# --------------------------------------------------
# Generate AI plant-care response
# --------------------------------------------------

def generate_plant_advice(ai_context):
    """
    Send GreenPulse plant information to Gemini
    and return an AI-generated care explanation.
    """

    prompt = f"""
You are the GreenPulse AI plant-care assistant.

Analyze the following plant information.

{ai_context}

Provide a short and practical plant-care explanation.

Your response should:

1. Explain the current plant condition.
2. Consider the current sensor readings.
3. Consider the historical trends.
4. Consider the weather information.
5. Respect the decision engine result.
6. Give a practical recommendation.
7. Do not invent sensor measurements.
8. Do not override the decision engine status.

Keep the response clear and suitable for a normal plant owner.
"""

    response = llm.invoke(prompt)

    # --------------------------------------------------
    # Extract only the generated text from Gemini's response
    # --------------------------------------------------

    if isinstance(response.content, list):
        text_parts = []

        for block in response.content:
            if isinstance(block, dict) and block.get("type") == "text":
                text_parts.append(block.get("text", ""))

        return "\n".join(text_parts).strip()

    return str(response.content).strip()

