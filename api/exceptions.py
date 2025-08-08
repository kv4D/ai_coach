"""Custom exceptions and their status codes for the API."""
from fastapi.responses import JSONResponse
from fastapi import Request

class BaseCustomException(Exception):
    """Base exception for all API errors."""
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status = status_code
        
        super().__init__(self.message)

class NotFoundError(BaseCustomException):
    """Resource not found error."""
    def __init__(self, message: str = "Not found"):
        super().__init__(message, status_code=404)

class AlreadyExistError(BaseCustomException):
    """Resource already exists error."""
    def __init__(self, message: str = "Already exists"):
        super().__init__(message, status_code=409)

class ValidationError(BaseCustomException):
    """Data validation error."""
    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status_code=400)

class UnexpectedError(BaseCustomException):
    """Unidentified error.

    Use for unexpected exceptions that are not processed.
    """
    def __init__(self, message: str = "Unexpected error"):
        super().__init__(message, status_code=500)


async def custom_error_handler(request: Request,
                               exc: BaseCustomException) -> JSONResponse:
    """
    Handle all custom exceptions.
    
    All defined exceptions in `exceptions.py` will be handled here.
    """
    return JSONResponse(
        status_code=exc.status,
        content={
            "message": exc.message,
            "type": exc.__class__.__name__,  
            "detail": str(exc)
            }
        )

# import this to use for exception handling
exception_handlers = {
    BaseCustomException: custom_error_handler
}
