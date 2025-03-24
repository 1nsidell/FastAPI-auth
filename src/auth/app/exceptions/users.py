from typing import Optional

from auth.core.exceptions import BaseCustomException


class CustomUsersException(BaseCustomException):
    """Base class for all user-related exceptions."""

    pass


class UserNotFoundException(CustomUsersException):
    """User not found."""

    error_type = "USER_NOT_FOUND"
    status_code = 404

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class UserAlreadyExistException(CustomUsersException):
    """User already exists."""

    error_type = "USER_EXIST"
    status_code = 409

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)
