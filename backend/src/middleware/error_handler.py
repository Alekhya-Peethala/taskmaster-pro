"""
TaskMaster Pro - Error Handling Middleware
Generated with GitHub Copilot assistance
Global exception handling for FastAPI application
Provides consistent error responses per API contract (Principle V)
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from typing import Union

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Handle HTTP exceptions and return consistent JSON error responses.
    
    Args:
        request: FastAPI request object
        exc: HTTP exception raised
        
    Returns:
        JSONResponse with error details
    """
    logger.error(
        f"HTTP {exc.status_code} error on {request.method} {request.url.path}: {exc.detail}"
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """
    Handle Pydantic validation errors with detailed field-level errors.
    
    Args:
        request: FastAPI request object
        exc: Pydantic validation exception
        
    Returns:
        JSONResponse with validation error details
    """
    logger.warning(
        f"Validation error on {request.method} {request.url.path}: {exc.errors()}"
    )
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": exc.errors()
        }
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unexpected exceptions with generic error response.
    Logs the full exception for debugging while returning safe message to client.
    
    Args:
        request: FastAPI request object
        exc: Generic exception
        
    Returns:
        JSONResponse with generic error message
    """
    logger.exception(
        f"Unexpected error on {request.method} {request.url.path}: {str(exc)}"
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error. Please try again later."
        }
    )


def register_exception_handlers(app) -> None:
    """
    Register all exception handlers with the FastAPI app.
    
    Usage in main.py:
        from src.middleware.error_handler import register_exception_handlers
        register_exception_handlers(app)
    """
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
