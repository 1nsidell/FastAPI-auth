from __future__ import annotations
import logging
import uuid
from typing import Any, Self, TYPE_CHECKING

import httpx

from auth.app.gateways import UsersManagementGatewayProtocol
from auth.app.schemas.users import SInfoUser


if TYPE_CHECKING:
    from auth.settings import Settings

log = logging.getLogger("app")


class UsersManagementV1GatewayImpl(UsersManagementGatewayProtocol):
    def __init__(
        self: Self,
        settings: Settings,
        client: httpx.AsyncClient,
    ) -> None:
        self.settings = settings
        self.client = client

    async def get_user_info(self: Self, user_id: int) -> SInfoUser:
        request_id = str(uuid.uuid4())
        header_id = {"X-Request-ID": request_id}
        log.info(
            "Requesting data with id: %s from UsersManagement - ID: %s.",
            user_id,
            request_id,
        )
        response = await self.client.get(
            url=f"/v1/users/{user_id}", headers=header_id
        )
        response.raise_for_status()
        data = response.json()
        log.info(
            "Successful request for data with id: %s from UsersManagement - ID: %s.",
            user_id,
            request_id,
        )
        return SInfoUser.model_validate(data, from_attributes=True)

    async def create_user_info(self: Self, **data: Any) -> SInfoUser:
        request_id = str(uuid.uuid4())
        header_id = {"X-Request-ID": request_id}
        log.info(
            "Request to create a data: %s in UsersManagement - ID: %s.",
            data,
            header_id,
        )
        response = await self.client.post(
            url="/v1/users", json=data, headers=header_id
        )
        response.raise_for_status()
        response_data = response.json()
        log.info(
            "User: %s was successfully created in UsersManagement - ID: %s.",
            data,
            header_id,
        )
        return SInfoUser.model_validate(response_data, from_attributes=True)

    async def update_user(self: Self, user_id: int, **data: Any) -> None:
        pass

    async def delete_user(self: Self, **data: Any) -> None:
        request_id = str(uuid.uuid4())
        header_id = {"X-Request-ID": request_id}
        log.info(
            "Request to delete user: %s in UsersManagement - ID: %s.",
            data,
            header_id,
        )
        await self.client.delete(url="/v1/users", json=data, headers=header_id)
        log.info(
            "User: %s was successfully deleted in UsersManagement - ID: %s.",
            data,
            header_id,
        )
