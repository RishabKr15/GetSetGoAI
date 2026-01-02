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
        # Try exchangerate-api.com first if api_key provided
        if self.api_key:
            url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/{from_currency}"
            try:
                response = requests.get(url, timeout=10)
            except requests.RequestException as e:
                # fall through to fallback provider
                response = None

            if response is not None and response.status_code == 200:
                data = response.json()
                rates = data.get('conversion_rates') or data.get('rates')
                if not rates:
                    raise RuntimeError("Currency API response missing conversion rates")
                if to_currency not in rates:
                    raise ValueError(f"Invalid target currency code: {to_currency}")
                rate = rates[to_currency]
                return amount * rate

        # Fallback: use exchangerate.host (no API key required, free)
        try:
            fallback_url = f"https://api.exchangerate.host/latest?base={from_currency}&symbols={to_currency}"
            resp2 = requests.get(fallback_url, timeout=10)
        except requests.RequestException as e:
            raise ConnectionError(f"Currency API requests failed: {e}")

        if resp2.status_code != 200:
            try:
                err = resp2.json()
            except Exception:
                err = resp2.text
            raise RuntimeError(f"Fallback currency API returned status {resp2.status_code}: {err}")

        data2 = resp2.json()
        rates2 = data2.get('rates')
        if not rates2 or to_currency not in rates2:
            raise ValueError(f"Invalid target currency code or missing rate from fallback provider: {to_currency}")
        rate2 = rates2[to_currency]
        return amount * rate2