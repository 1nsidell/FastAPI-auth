from abc import abstractmethod
from typing import Any, Protocol, Self

from auth.app.schemas.users import SInfoUser


class UsersManagementGatewayProtocol(Protocol):

    @abstractmethod
    async def get_user_info(self: Self, user_id: int) -> SInfoUser: ...

    @abstractmethod
    async def create_user_info(self: Self, **data: Any) -> None: ...

    @abstractmethod
    async def update_user(self: Self, **data: Any) -> None: ...

    @abstractmethod
    async def delete_user(self: Self, **data: Any) -> None: ...
