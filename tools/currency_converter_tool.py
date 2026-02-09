from langchain_core.runnables import RunnableConfig

class CurrencyConverterTool:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("EXCHANGE_API_KEY")
        self.currency_service = CurrencyConverter(self.api_key)
        self.currency_tools_list = self._setup_tools()
        
    def _setup_tools(self):
        """setup all the tools for once currency to another"""
        @tool
        async def convert_currency(amount: float, from_currency: str, to_currency: str, config: RunnableConfig):
            """convert amount from one currency to another"""
            api_keys = config.get("configurable", {}).get("api_keys", {})
            user_key = api_keys.get("exchange_api_key")
            
            try:
                result = await self.currency_service.convert(amount, from_currency, to_currency, api_key=user_key)
                return result
            except Exception as e:
                # Return a readable error message instead of crashing
                return f"Currency conversion failed: {e}"
            
        return [convert_currency]




    