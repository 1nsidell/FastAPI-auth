from __future__ import annotations
import logging
from typing import TYPE_CHECKING

import aio_pika

from auth.app.exceptions.gateway import RMQChannelMissing

if TYPE_CHECKING:
    from auth.settings import Settings


log = logging.getLogger("app")


class RMQManagerImpl:
    def __init__(self, settings: Settings):
        self.__settings = settings

        self.__connection: aio_pika.Connection
        self.__channel: aio_pika.Channel

    @property
    def channel(self) -> aio_pika.Channel:
        if not self.__channel:
            raise RMQChannelMissing()
        return self.__channel

    async def startup(self):
        self.__connection = await aio_pika.connect_robust(
            url=self.__settings.rmq.url
        )
        log.info("Created RMQ connect [%s].", id(self.__connection))
        self.__channel = await self.__connection.channel()
        log.info("Created RMQ channel [%s].", id(self.__channel))

    async def shutdown(self):
        if self.__channel:
            await self.__channel.close()
        if self.__connection:
            await self.__connection.close()
