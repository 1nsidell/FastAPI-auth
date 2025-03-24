from __future__ import annotations
import json
from typing import Dict, TYPE_CHECKING
import aio_pika
from auth.app.gateways import NotificationsManagerProtocol


if TYPE_CHECKING:
    from auth.settings import Settings


class NotificationsManagerImpl(NotificationsManagerProtocol):
    def __init__(self, channel: aio_pika.Channel, settings: Settings) -> None:
        self.__channel = channel
        self.__settings = settings

    async def send_email_notifications(self, data: Dict) -> None:
        message_body = json.dumps(data).encode()
        await self.__channel.default_exchange.publish(
            aio_pika.Message(
                body=message_body,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=self.__settings.rmq.RABBIT_EMAIL_QUEUE,
        )
