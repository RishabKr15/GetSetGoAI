
class Calculator:
    
    @staticmethod
    def multiply(num1 : int, num2 : int) -> int:
        """
        Multiply two numbers together.

        This function takes two numbers as input and returns their product.

        Args:
            num1 (int or float): The first number
            num2 (int or float): The second number

        Returns:
            int: The product of num1 and num2
        """
        
        # Multiply the two numbers together
        result = num1 * num2
        
        # Return the result
        return result
    @staticmethod
    def add(num1 : int, num2 : int) -> int:
        """
        Add two numbers together.

        This function takes two numbers as input and returns their sum.

        Args:
            num1 (int or float): The first number
            num2 (int or float): The second number

        Returns:
            int: The sum of num1 and num2
        """
        
        # Add the two numbers together
        result = num1 + num2
        
        # Return the result
        return result
    
    @staticmethod
    def calculate_total(*x: float)->float:
        """
        Calculate the total of multiple values.

        This function takes in a variable number of arguments and adds them all together.

        Args:
            *x (float): The values to add together

        Returns:
            float: The total of all the provided values
        """
        return sum(x)
    
    @staticmethod
    def calculate_daily_budget(total :float, days:int)->float:
        """
        Calculate the daily budget.

        This function takes in a total amount and the number of days to divide it by.

        Args:
            total (float): The total amount to divide.
            days (int): The number of days to divide the total by.

        Returns:
            float: The daily budget.
        """
        return total/days if days>0 else 0
    
    
        
    