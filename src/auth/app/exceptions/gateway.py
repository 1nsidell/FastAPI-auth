from typing import Optional

from auth.core.exceptions import BaseCustomException


class CastomGatewayException(BaseCustomException):
    """Base class for exceptions with gateways."""

    pass


class RMQChannelMissing(CastomGatewayException):
    """RabbitMQ channel missing."""

    error_type = "CHANNEL_MISSING"
    status_code = 500

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)
