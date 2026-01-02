import os
import json
from typing import Any, Dict
try:
    from langchain_community.utilities import SerpAPIWrapper
except ImportError:
    SerpAPIWrapper = None
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
load_dotenv()

# Known parked or junk domains that often appear in search results for dead businesses
JUNK_DOMAINS = [
    "hugedomains.com",
    "dan.com",
    "afternic.com",
    "godaddy.com",
    "domainmarket.com",
    "sedo.com"
]

def is_junk_link(link: str) -> bool:
    """Check if a link is from a known junk or parked domain."""
    if not link:
        return True
    return any(domain in link.lower() for domain in JUNK_DOMAINS)

class SerpAPISearchTool:
    def __init__(self, api_key: str):
        if SerpAPIWrapper is None:
            raise ImportError("SerpAPI not available. Install with: pip install google-search-results")
        self.search_wrapper = SerpAPIWrapper(serpapi_api_key=api_key)

    def _format_serp_results(self, search_query: str) -> str:
        """Helper to run search and format results with links"""
        results = self.search_wrapper.results(search_query)
        formatted_results = []
        
        # Check organic results
        organic = results.get("organic_results", [])
        for res in organic[:5]:
            title = res.get("title")
            link = res.get("link")
            if title and link:
                formatted_results.append(f"{title}: {link}")
        
        # Check local results (often present for places)
        local = results.get("local_results", {}).get("places", [])
        for res in local[:5]:
            title = res.get("title")
            link = res.get("links", {}).get("website") or res.get("link")
            if title and link:
                formatted_results.append(f"{title}: {link}")

        if not formatted_results:
             return self.search_wrapper.run(search_query) # Fallback to string
        
        # Sort to prioritize certain high-quality domains like Tripadvisor, Zomato, Official sites
        # but for now, just filtering junk out is enough.
        clean_results = [res for res in formatted_results if not is_junk_link(res.split(": ")[-1])]
        
        if not clean_results and formatted_results:
            return "\n".join(formatted_results[:2]) # Fallback if everything looks junk (rare)
            
        return "\n".join(clean_results[:5])

    def search_attractions(self, place: str) -> str:
        """
        Search for top attractions in and around a given place.
        """
        return self._format_serp_results(f"official attractions and things to do in {place} with website links")

    def search_restaurants(self, place: str) -> str:
        """
        Search for top restaurants in and around a given place.
        """
        return self._format_serp_results(f"top restaurants in {place} official website or tripadvisor zomato")

    def search_hotels(self, place: str) -> str:
        """
        Search for top hotels in and around a given place.
        """
        return self._format_serp_results(f"best hotels in {place} official website or booking.com tripadvisor")

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
    
    def _format_tavily_results(self, result: Any) -> str:
        """Helper to format Tavily results into Name: URL string"""
        results_list = []
        if isinstance(result, list):
            results_list = result
        elif isinstance(result, dict):
            results_list = result.get("results", [])
        
        if results_list:
            formatted = []
            for res in results_list[:5]:
                if isinstance(res, dict):
                    title = res.get("title")
                    url = res.get("url")
                    if title and url:
                        formatted.append(f"{title}: {url}")
            if formatted:
                clean_formatted = [res for res in formatted if not is_junk_link(res.split(": ")[-1])]
                return "\n".join(clean_formatted[:5]) if clean_formatted else "\n".join(formatted[:2])
        return str(result)

    def search_attractions(self, place: str)->str:
        """
        Search for top attractions in and around a given place.
        """
        tavily_tool = TavilySearch(topic="general", search_depth='advanced')
        result = tavily_tool.invoke({"query": f"verified top attractions and landmarks in {place} official website"})
        return self._format_tavily_results(result)

    def tavily_search_restaurants(self, place: str)->str:
        """
        Search for top restaurants in and around a given place.
        """
        tavily_tool = TavilySearch(topic="general", search_depth='advanced')
        result = tavily_tool.invoke({"query": f"top rated restaurants in {place} official website zomato tripadvisor"})
        return self._format_tavily_results(result)

    def tavily_search_activity(self, place :str)->str:
        """
        Search for top activities in and around a given place.
        """
        tavily_tool = TavilySearch(topic="general", search_depth='advanced')
        result = tavily_tool.invoke({"query": f"tourist activities and experiences in {place} verified links"})
        return self._format_tavily_results(result)
    
    def tavily_search_transportation(self, place :str)->str:
        """
        Searches for available modes of transportation in and around a given place.
        """
        tavily_tool = TavilySearch(topic="general", search_depth='advanced')
        result = tavily_tool.invoke({"query": f"official public transport and taxi guide for {place}"})
        return self._format_tavily_results(result)

    def tavily_search_hotels(self, place: str) -> str:
        """
        Search for top hotels in and around a given place.
        """
        tavily_tool = TavilySearch(topic="general", search_depth='advanced')
        result = tavily_tool.invoke({"query": f"top luxury and boutique hotels in {place} official website booking.com"})
        return self._format_tavily_results(result)
