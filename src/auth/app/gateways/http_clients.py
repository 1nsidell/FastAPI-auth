from __future__ import annotations
from typing import Self, Optional, TYPE_CHECKING

import httpx

from auth.app.gateways import users_management_headers

if TYPE_CHECKING:
    from auth.settings import Settings


class HTTPUsersManagementClient:
    def __init__(self: Self, settings: Settings):
        self.__settings = settings
        self.__client: Optional[httpx.AsyncClient]

    def startup(self: Self):
        self.__client = httpx.AsyncClient(
            base_url=self.__settings.gateways.USERS_MANAGEMENT,
            headers=users_management_headers,
            timeout=self.__settings.gateways.REQUEST_TIMEOUT,
        )

    @property
    def client(self) -> httpx.AsyncClient:
        return self.__client

    async def shutdown(self: Self):
        if self.client:
            await self.client.aclose()
