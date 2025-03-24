"""
ioc container for creating services.
"""

from typing import Annotated

from fastapi import Depends

from auth.app.depends import (
    JWTProvider,
    NotificationsManager,
    UsersManagementV1Gateway,
)
from auth.app.depends.providers import JWTProvider, PassProvider
from auth.app.depends.repositories import UsersSQLRepository
from auth.app.services import AuthServiceProtocol
from auth.app.services.impls.notifications import NotificationsServiceImpl
from auth.app.services.protocols.notifications_protocol import (
    NotificationsServiceProtocol,
)
from auth.core import UoW
from auth.core.depends import SettingsService

from ..services.impls.auth import AuthServiceImpl


def get_auth_service(
    users_sql_repository: UsersSQLRepository,
    users_management_gateway: UsersManagementV1Gateway,
    pass_provider: PassProvider,
    jwt_provider: JWTProvider,
    uow: UoW,
) -> AuthServiceProtocol:
    return AuthServiceImpl(
        users_sql_repository=users_sql_repository,
        users_management_gateway=users_management_gateway,
        pass_provider=pass_provider,
        jwt_provider=jwt_provider,
        uow=uow,
    )


AuthService = Annotated[AuthServiceProtocol, Depends(get_auth_service)]


def get_notifications_service(
    settings: SettingsService,
    notifications_manager: NotificationsManager,
    jwt_provider: JWTProvider,
) -> NotificationsServiceProtocol:
    return NotificationsServiceImpl(
        settings=settings,
        notifications_manager=notifications_manager,
        jwt_provider=jwt_provider,
    )


NotificationsService = Annotated[
    NotificationsServiceProtocol, Depends(get_notifications_service)
]
