from typing import Optional

from auth.core.exceptions import BaseCustomException


class CustomDataException(BaseCustomException):
    """Base class for exceptions with data."""

    pass


class DataNotTransmittedException(CustomDataException):
    """The data was not transmitted."""

    error_type = "MISSING DATA"
    status_code = 400

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class PasswordNotMatchException(CustomDataException):
    """The passwords entered do not match."""

    error_type = "PASSWORD NOT MATCH"
    status_code = 409

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)
