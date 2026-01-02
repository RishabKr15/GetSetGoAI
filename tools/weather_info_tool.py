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
        def get_current_weather(city: str) -> str:
            """Get current weather conditions for a city."""
            weather_data = self.weather_service.get_weather(city)
            if weather_data and "main" in weather_data:
                temp = weather_data['main'].get('temp', 'N/A')
                desc = weather_data.get('weather', [{}])[0].get('description', 'N/A')
                humidity = weather_data['main'].get('humidity', 'N/A')
                wind = weather_data.get('wind', {}).get('speed', 'N/A')
                resolved_name = weather_data.get('name', city)
                return f"Current Weather in {resolved_name}: {temp}°C, {desc} (Humidity: {humidity}%, Wind: {wind} m/s)"
            return f"Couldn't fetch current weather for {city}."

        @tool
        def get_weather_forecast(city: str) -> str:
            """Get a summarized 5-day weather forecast for a city."""
            forecast_data = self.weather_service.get_weather_forecast(city)
            if forecast_data and 'list' in forecast_data:
                # Group by day and get min/max
                daily_stats = {}
                for entry in forecast_data['list']:
                    date = entry['dt_txt'].split(' ')[0]
                    temp = entry['main']['temp']
                    if date not in daily_stats:
                        daily_stats[date] = {'min': temp, 'max': temp, 'desc': entry['weather'][0]['description']}
                    else:
                        daily_stats[date]['min'] = min(daily_stats[date]['min'], temp)
                        daily_stats[date]['max'] = max(daily_stats[date]['max'], temp)
                
                summary = [f"5-Day Forecast for {city}:"]
                for date, stats in list(daily_stats.items())[:5]:
                    summary.append(f"- {date}: High {stats['max']}°C, Low {stats['min']}°C ({stats['desc']})")
                
                return "\n".join(summary)
            return f"Couldn't fetch forecast for {city}."
    
        return [get_current_weather, get_weather_forecast]
           