import requests
from dotenv import load_dotenv
load_dotenv()
import os

class CurrencyConverter:
    def __init__(self, api_key:str):
        """
        Initialize the CurrencyConverter class with the API key.

        Parameters:
            api_key (str): API key from exchangerate-api.com
        """
        self.api_key = api_key
        self.base_url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest'

    
    def convert(self, amount:float,from_currency: str, to_currency: str)->float:
        """
        Convert a given amount from one currency to another.

        Parameters:
            amount (float): amount of money to convert
            from_currency (str): currency code of the original currency
            to_currency (str): currency code of the currency to convert to

        Returns:
            The converted amount if successful, None otherwise
        """
        url = f"{self.base_url}/{from_currency}"
        response = requests.get(url)
        if response.status_code != 200:
            return None
        data = response.json()['conversion_rates']
        if to_currency not in data:
            raise ValueError(f"Invalid currency code: {to_currency}")
        rate = data[to_currency]
        return amount * rate