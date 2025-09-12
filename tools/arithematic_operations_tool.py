import os
from dotenv import load_dotenv
from langchain.tools import tool
load_dotenv()
from langchain_community.utilities import AlphaVantageAPIWrapper

class ArithematicOperationsTool():
    def __init__(self):
        self.calculater_tools_list = self._setup_tools()
        
    def _setup_tools(self):
        @tool
        def multiply(a: float, b: float) -> float:
            """
            Multiply two numbers together.

            Args:
                a: The first number
                b: The second number

            Returns:
                The product of a and b
            """
            return a * b
            
        @tool
        def add(a: float, b: float) -> float:
            """
            Add two numbers together.

            Args:
                a: The first number
                b: The second number

            Returns:
                The sum of a and b
            """
            return a + b
            
        @tool
        def subtract(a: float, b: float) -> float:
            """
            Subtract two numbers.

            Args:
                a: The first number
                b: The second number

            Returns:
                The difference of a and b
            """
            return a - b
            
        @tool
        def divide(a: float, b: float) -> float:
            """
            Divide two numbers.

            Args:
                a: The first number (dividend)
                b: The second number (divisor)

            Returns:
                The quotient of a and b
            """
            if b == 0:
                return "Error: Division by zero"
            return a / b
            
        return [multiply, add, subtract, divide]

