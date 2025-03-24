from typing import Self

from auth.app.exceptions.security import AccessDeniedException
from auth.app.providers import APIAccessProviderProtocol


class APIAccessProviderImpl(APIAccessProviderProtocol):
    def __init__(self: Self, valid_api_key: str):
        self.valid_api_key = valid_api_key

    def check_api_key(self: Self, api_key: str):
        if api_key != self.valid_api_key:
            raise AccessDeniedException()
