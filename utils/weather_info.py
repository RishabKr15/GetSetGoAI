import httpx
import os

class WeatherInfoTool:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("WEATHER_API_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5/"

    async def get_weather(self, city: str, api_key: str = None):
        try:
            params = {
                "appid": api_key or self.api_key,
                "q": city,
                "units": "metric"
            }
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}weather", params=params)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {"error": str(e)}

    async def get_weather_forecast(self, city: str, api_key: str = None):
        try:
            params = {
                "appid": api_key or self.api_key,
                "q": city,
                "cnt": 40,  # 5 days * 8 (3-hour intervals)
                "units": "metric"
            }
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}forecast", params=params)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {"error": str(e)}
