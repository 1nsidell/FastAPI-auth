from __future__ import annotations
from typing import TYPE_CHECKING

from auth.app.gateways import NotificationsManagerProtocol
from auth.app.providers import JWTProviderProtocol
from auth.app.schemas.users import SInfoUser
from auth.app.services import NotificationsServiceProtocol


if TYPE_CHECKING:
    from auth.settings import Settings


class NotificationsServiceImpl(NotificationsServiceProtocol):

    def __init__(
        self,
        settings: Settings,
        notifications_manager: NotificationsManagerProtocol,
        jwt_provider: JWTProviderProtocol,
    ):
        self.settings = settings
        self.notifications_manager = notifications_manager
        self.jwt_provider = jwt_provider

    async def send_confirm_email(
        self, email: str, user_info: SInfoUser
    ) -> None:
        token = self.jwt_provider.create_refresh_token(user_info)
        body = {
            "type": "confirm_email",
            "recipient": email,
            "token": token,
        }
        await self.notifications_manager.send_email_notifications(body)

    async def send_recovery_password(
        self, email: str, user_info: SInfoUser
    ) -> None:
        token = self.jwt_provider.create_refresh_token(user_info)
        body = {
            "type": "recovery_password",
            "recipient": email,
            "token": token,
        }
        await self.notifications_manager.send_email_notifications(body)
