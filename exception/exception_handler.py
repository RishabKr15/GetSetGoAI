import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exception.exceptions import BaseAppException, ProviderAPIError

logger = logging.getLogger(__name__)

def register_exception_handlers(app: FastAPI):
    """Register all custom exception handlers to the FastAPI app."""

    @app.exception_handler(BaseAppException)
    async def base_app_exception_handler(request: Request, exc: BaseAppException):
        logger.error(f"App Exception: {exc.message}", exc_info=True)
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.message}
        )

    @app.exception_handler(ProviderAPIError)
    async def provider_api_exception_handler(request: Request, exc: ProviderAPIError):
        logger.error(f"Provider API Error: {exc.message}")
        # Return specialized status code if needed, like 402 for credits
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": f"Provider API Error: {exc.message}"}
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.exception("Internal Server Error")
        return JSONResponse(
            status_code=500,
            content={"error": "An internal server error occurred. Please try again later."}
        )
