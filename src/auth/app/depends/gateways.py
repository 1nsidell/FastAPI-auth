from typing import Annotated

import aio_pika
import httpx
from fastapi import Depends

from auth.app.gateways import (
    HTTPUsersManagementClient,
    NotificationsManagerProtocol,
    UsersManagementGatewayProtocol,
)
from auth.app.gateways.notifications.impls.notifications import (
    NotificationsManagerImpl,
)
from auth.app.gateways.rmq_manager import RMQManagerImpl
from auth.app.gateways.users_management.v1.users_management import (
    UsersManagementV1GatewayImpl,
)
from auth.core import SettingsService
from auth.settings import Settings, settings


def get_users_management_client_manager(
    settings: Settings,
) -> HTTPUsersManagementClient:
    """Create an instance class to get a client Users Management microservice."""
    return HTTPUsersManagementClient(settings)


UsersManagementClientManager: HTTPUsersManagementClient = (
    get_users_management_client_manager(settings)
)


def get_user_management_client() -> httpx.AsyncClient:
    return UsersManagementClientManager.client


UsersManagementClient = Annotated[
    httpx.AsyncClient, Depends(get_user_management_client)
]


def get_rmq_manager(settings: Settings) -> RMQManagerImpl:
    return RMQManagerImpl(settings)


RMQManager: RMQManagerImpl = get_rmq_manager(settings=settings)


def get_rmq_channel() -> aio_pika.Channel:
    return RMQManager.channel


RMQChannel = Annotated[aio_pika.Channel, Depends(get_rmq_channel)]


def get_notifications_manager(
    channel: RMQChannel,
    settings: SettingsService,
) -> NotificationsManagerProtocol:
    return NotificationsManagerImpl(channel=channel, settings=settings)


NotificationsManager = Annotated[
    NotificationsManagerProtocol, Depends(get_notifications_manager)
]


def get_user_management_v1_gateway(
    settings: SettingsService,
    client: UsersManagementClient,
) -> UsersManagementGatewayProtocol:
    return UsersManagementV1GatewayImpl(settings, client)


UsersManagementV1Gateway = Annotated[
    UsersManagementGatewayProtocol, Depends(get_user_management_v1_gateway)
]
