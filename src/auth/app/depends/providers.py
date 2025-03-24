from typing import Annotated

from fastapi import Depends

from auth.app.providers import (
    APIAccessProviderProtocol,
    JWTProviderProtocol,
    PassProviderProtocol,
)
from auth.app.providers.impls.api_access import APIAccessProviderImpl
from auth.app.providers.impls.jwt import JWTProviderImpl
from auth.app.providers.impls.password import PassProviderImpl
from auth.settings import settings


def get_api_access_provider() -> APIAccessProviderProtocol:
    return APIAccessProviderImpl(settings.api_key)


APIAccessProvider = Annotated[
    APIAccessProviderProtocol, Depends(get_api_access_provider)
]


def get_jwt_provider() -> JWTProviderProtocol:
    return JWTProviderImpl()


JWTProvider = Annotated[JWTProviderProtocol, Depends(get_jwt_provider)]


def get_pass_provider() -> PassProviderProtocol:
    return PassProviderImpl()


PassProvider = Annotated[PassProviderProtocol, Depends(get_pass_provider)]
