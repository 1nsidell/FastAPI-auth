class BaseCustomException(Exception):
    """Base class for all custom exceptions."""

    error_type: str
    status_code: int
    message: str
