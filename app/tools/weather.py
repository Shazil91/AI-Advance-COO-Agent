import os
import requests
from app.tools.base import BaseTool

API_KEY = os.getenv("OPENWEATHER_API_KEY")


class GetWeather(BaseTool):

    def name(self):
        return "weather"

    def run(self, input: dict):

        city = input.get("city")

        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&units=metric"
        )

        response = requests.get(url)

        if response.status_code != 200:
            return "Weather not found."

        result = response.json()

        return {
            "city": city,
            "temperature": result["main"]["temp"],
            "humidity": result["main"]["humidity"],
            "condition": result["weather"][0]["description"],
        }