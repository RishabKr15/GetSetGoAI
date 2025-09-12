import requests
import os
from dotenv import load_dotenv
from utils.currency_converter import CurrencyConverter
from langchain.tools import tool

class CurrencyConverterTool:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("EXCHANGE_API_KEY")
        self.currency_service = CurrencyConverter(self.api_key)
        self.currency_tools_list = self._setup_tools()
        
    
    def _setup_tools(self):
        """setup all the tools for once currency to another"""
        @tool
        def convert_currency(amount: float,from_currency: str, to_currency: str):
            """convert amount from one currency to another"""
            return self.currency_service.convert(amount,from_currency, to_currency)
            
        return [convert_currency]




    