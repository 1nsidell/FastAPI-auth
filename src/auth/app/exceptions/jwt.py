from typing import Optional

from auth.core.exceptions import BaseCustomException


class CustomJWTException(BaseCustomException):
    """Base class for all JWT custom exceptions."""

    pass


class InvalidTokenException(CustomJWTException):
    """Invalid token."""

    error_type = "INVALID_TOKEN"
    status_code = 401

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class TokenTimeOutException(CustomJWTException):
    """Token has expired."""

    error_type = "TOKEN_EXPIRED"
    status_code = 401

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)
