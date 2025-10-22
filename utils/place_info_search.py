import os
import json
try:
    from langchain_community.utilities import SerpAPIWrapper
except ImportError:
    SerpAPIWrapper = None
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
load_dotenv()

class SerpAPISearchTool:
    def __init__(self, api_key: str):
        if SerpAPIWrapper is None:
            raise ImportError("SerpAPI not available. Install with: pip install google-search-results")
        self.search_wrapper = SerpAPIWrapper(serpapi_api_key=api_key)

    def search_attractions(self, place: str) -> str:
        """
        Search for top attractions in and around a given place.

        Args:
            place (str): Location to search around.

        Returns:
            str: Result of the search.
        """
        return self.search_wrapper.run(f"top attractions in and around {place}")

    def search_restaurants(self, place: str) -> str:
        """
        Search for top restaurants in and around a given place.

        Args:
            place (str): Location to search around.

        Returns:
            str: Result of the search.
        """
        return self.search_wrapper.run(f"top restaurants in and around {place}")

    def search_hotels(self, place: str) -> str:
        """
        Search for top hotels in and around a given place.

        Args:
            place (str): Location to search around.

        Returns:
            str: Result of the search.
        """
        return self.search_wrapper.run(f"top hotels in and around {place}")

    def search_activity(self, place: str) -> str:
        """
        Search for top activities in and around a given place.

        Args:
            place (str): Location to search around.

        Returns:
            str: Result of the search.
        """
        return self.search_wrapper.run(f"top activities in and around {place}")

    def search_transportation(self, place: str) -> str:
        """
        Searches for available modes of transportation in and around a given place.

        Args:
            place (str): Location to search around.

        Returns:
            str: Result of the search.
        """
        return self.search_wrapper.run(f"modes of transportation in and around {place}")
class TavilySearchTool:
    def __init__(self, api_key : str):
        from langchain_tavily import TavilySearch
        self.tavily_wrapper = TavilySearch(tavily_api_key=api_key)
    
    def search_attractions(self, place: str)->dict:
        """
        Search for top attractions in and around a given place.

        Args:
            place (str): location to search around

        Returns:
            dict: result of the search
        """
        tavily_tool = TavilySearch(topic="general",include_answer= 'advanced')
        result = tavily_tool.invoke({"query": f"top attraction in and around {place}"})
        if isinstance(result,dict) and result.get("answer"):
            return result["answer"]
        else:
            return result
    def tavily_search_restaurants(self, place: str)->dict:
        """
        Search for top restaurants in and around a given place.

        Args:
            place (str): location to search around

        Returns:
            dict: result of the search
        """
        tavily_tool = TavilySearch(topic="general",include_answer= 'advanced')
        result = tavily_tool.invoke({"query": f"top 10 restaurants in and around {place}"})
        if isinstance(result,dict) and result.get("answer"):
            return result["answer"]
        else:
            return result
    def tavily_search_activity(self,place :str)->dict:
        """
        Search for top activities in and around a given place.

        Args:
            place (str): location to search around

        Returns:
            dict: result of the search
        """
        tavily_tool = TavilySearch(topic="general",include_answer= 'advanced')
        result = tavily_tool.invoke({"query": f"top activities in and around {place}"})
        if isinstance(result,dict) and result.get("answer"):
            return result["answer"]
        else:
            return result
    
    def tavily_search_transportation(self,place :str)->dict:
        """
        Searches for available modes of transportation in and around a given place.

        Args:
            place (str): location to search around

        Returns:
            dict: result of the search
        """
        tavily_tool = TavilySearch(topic="general",include_answer= 'advanced')
        result = tavily_tool.invoke({"query": f"what are the different modes of transportation in {place}"})
        if isinstance(result,dict) and result.get("answer"):
            return result["answer"]
        else:
            return result