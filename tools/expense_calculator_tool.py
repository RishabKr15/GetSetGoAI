from utils.expense_calculator import Calculator
from typing import List
from langchain.tools import tool

class CalculatorTool:
    def __init__(self):
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self):
        """Set up the calculator tools."""
        @tool
        async def estimate_hotel_cost(price_per_night: int, total_days: float) -> float:
            """Estimate the total cost of a hotel stay."""
            return self.calculator.multiply(price_per_night, total_days)
        @tool
        async def calculate_total_expense(price_per_ticket: float, total_days: float) -> float:
            """Estimate the total cost of trip."""
            return self.calculator.multiply(price_per_ticket, total_days)
        @tool
        async def calculate_daily_budget(total_cost: float, days: int) -> float:
            """Calculate the daily budget for a trip."""
            return self.calculator.calculate_daily_budget(total_cost, days)
        return [estimate_hotel_cost, calculate_total_expense, calculate_daily_budget]