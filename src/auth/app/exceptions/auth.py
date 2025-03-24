from typing import Optional

from auth.core.exceptions import BaseCustomException


class CustomAuthException(BaseCustomException):
    """Base class for all AUTH custom exceptions."""

    pass


class IncorrectPasswordException(CustomAuthException):
    """The password entered is incorrect."""

    error_type = "INCORRECT_PASSWORD"
    status_code = 401

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class UserBlockedException(CustomAuthException):
    """User blocked."""

    error_type = "USER_BLOCKED"
    status_code = 403

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)
