import os

import requests
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
print("API key loaded:", bool(OPENWEATHER_API_KEY))

def get_current_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    response.raise_for_status()

    return response.json()


def get_weather_forecast(city):
    url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    response.raise_for_status()

    return response.json()


def is_rain_expected(city):
    forecast = get_weather_forecast(city)

    for item in forecast["list"][:8]:
        condition = item["weather"][0]["main"].lower()

        if "rain" in condition:
            return True

    return False

if __name__ == "__main__":
    rain_expected = is_rain_expected("Kurunegala")

    print(f"\nRain expected: {rain_expected}")