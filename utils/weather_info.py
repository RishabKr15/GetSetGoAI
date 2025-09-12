import requests
import os

class WeatherInfoTool:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("WEATHER_API_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5/"

    def get_weather(self, city):
        try:
            params = {
                "appid": self.api_key,
                "q": city,
                "units": "metric"
            }
            response = requests.get(f"{self.base_url}weather", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_weather_forecast(self, city):
        try:
            params = {
                "appid": self.api_key,
                "q": city,
                "cnt": 40,  # 5 days * 8 (3-hour intervals)
                "units": "metric"
            }
            response = requests.get(f"{self.base_url}forecast", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
