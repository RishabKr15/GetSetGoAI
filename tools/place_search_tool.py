import os
from utils.place_info_search import SerpAPISearchTool,TavilySearchTool
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv

class LocationInfoTool:
    def __init__(self):
        load_dotenv()
        serp_api_key = os.getenv("SERPAPI_API_KEY")
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        try:
            self.serp_tool = SerpAPISearchTool(api_key=serp_api_key) if serp_api_key else None
        except ImportError:
            print("⚠️  SerpAPI not available, using Tavily only")
            self.serp_tool = None
        self.tavily_tool = TavilySearchTool(api_key=tavily_api_key) if tavily_api_key else None
        self.place_search_tools_list = self._setup_tools()
        
    def _setup_tools(self) -> List:
        """Setup all the tools for place search"""
        
        @tool
        def search_attractions(place: str) -> str:
            """Search for top attractions in and around a given place"""
            if self.serp_tool:
                return self.serp_tool.search_attractions(place)
            elif self.tavily_tool:
                return self.tavily_tool.search_attractions(place)
            return "No search API available"
            
        @tool
        def search_restaurants(place: str) -> str:
            """Search for top restaurants in and around a given place"""
            if self.serp_tool:
                return self.serp_tool.search_restaurants(place)
            elif self.tavily_tool:
                return self.tavily_tool.tavily_search_restaurants(place)
            return "No search API available"
            
        @tool
        def search_hotels(place: str) -> str:
            """Search for top hotels in and around a given place"""
            if self.serp_tool:
                return self.serp_tool.search_hotels(place)
            elif self.tavily_tool:
                return self.tavily_tool.tavily_search_hotels(place)
            return "No search API available"
            
        @tool
        def search_activities(place: str) -> str:
            """Search for top activities in and around a given place"""
            if self.serp_tool:
                return self.serp_tool.search_activity(place)
            elif self.tavily_tool:
                return self.tavily_tool.tavily_search_activity(place)
            return "No search API available"
            
        @tool
        def search_transportation(place: str) -> str:
            """Search for transportation options in and around a given place"""
            if self.serp_tool:
                return self.serp_tool.search_transportation(place)
            elif self.tavily_tool:
                return self.tavily_tool.tavily_search_transportation(place)
            return "No search API available"
            
        return [search_attractions, search_restaurants, search_hotels, search_activities, search_transportation]
    