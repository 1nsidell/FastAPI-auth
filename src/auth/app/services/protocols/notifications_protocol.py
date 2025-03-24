from abc import abstractmethod
from typing import Protocol

from auth.app.gateways import NotificationsManagerProtocol
from auth.app.schemas.users import SInfoUser


class NotificationsServiceProtocol(Protocol):

    notifications_manager: NotificationsManagerProtocol

    @abstractmethod
    async def send_confirm_email(
        self,
        email: str,
        user_info: SInfoUser,
    ) -> None: ...

    @abstractmethod
    async def send_recovery_password(
        self,
        email: str,
        user_info: SInfoUser,
    ) -> None: ...
