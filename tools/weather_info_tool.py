import os
from typing import List, Any,Dict, Optional
from dotenv import load_dotenv
from utils.weather_info import WeatherInfoTool
from langchain.tools import tool



class WeatherInfoTool():
    def __init__(self,):
        load_dotenv()
        self.api_key = os.environ.get("WEATHER_API_KEY")
        from utils.weather_info import WeatherInfoTool as WeatherService
        self.weather_service = WeatherService(self.api_key)
        self.weather_tools_list = self._setup_tools()
    
    def _setup_tools(self) -> List:
        "Setup all the tools for the agent"
        
        @tool
        def get_current_weather(city : str)-> str:
            """get weather for current city"""
            weather_data = self.weather_service.get_weather(city)
            if weather_data:
                temp = weather_data.get('main',{}).get('temp','N/A')
                desc = weather_data.get('weather',[{}])[0].get('description','N/A')
                return f"Weather in {city}:\nTemperature: {temp}°C\nDescription: {desc}"
            return f"coudmn't fetch the weather for {city}"
        
        @tool
        def get_weather_forecast(city: str)->str:
            """get weather forecat for current city"""
            forecast_data = self.weather_service.get_weather_forecast(city)
            if forecast_data and 'list' in forecast_data:
                forecast_list = forecast_data['list']
                forecast_str = f"Weather forecast for {city}:\n"
                for forecast in forecast_list:
                    date = forecast['dt_txt']
                    temp = forecast['main']['temp']
                    desc = forecast['weather'][0]['description']
                    forecast_str += f"\nDate: {date}\nTemperature: {temp}°C\nDescription: {desc}"
                return forecast_str
    
        return [get_current_weather, get_weather_forecast]
           