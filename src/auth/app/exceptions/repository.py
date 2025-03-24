from typing import Optional

from auth.core.exceptions import BaseCustomException


class CustomRepositoriesException(BaseCustomException):
    """Base class for all custom exception databases."""

    pass


class SQLRepositoryException(CustomRepositoriesException):
    """SQL repository working error."""

    error_type = "SQL_REPOSITORY_ERROR"
    status_code = 500

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class RedisCacheDBException(CustomRepositoriesException):
    """Cache operation failed."""

    error_type = "REDIS_ERROR"
    status_code = 202

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class TransactionException(CustomRepositoriesException):
    """Transaction error."""

    error_type = "TRANSACTION_ERROR"
    status_code = 500

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)
