class BaseAppException(Exception):
    """Base exception for all application-specific errors."""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class ProviderAPIError(BaseAppException):
    """Raised when an LLM provider (like OpenRouter/Google) returns an error."""
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code)

class ToolExecutionError(BaseAppException):
    """Raised when an agent tool fails to execute correctly."""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message, status_code)

class ConfigurationError(BaseAppException):
    """Raised when configuration issues (like missing API keys) are detected."""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message, status_code)
