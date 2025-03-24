from typing import Optional

from auth.core.exceptions import BaseCustomException


class CustomSecurityException(BaseCustomException):
    """Base class for all API security related exceptions."""

    pass


class AccessDeniedException(CustomSecurityException):
    """API key rejected."""

    error_type = "API_KEY_ERROR"
    status_code = 403

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)
