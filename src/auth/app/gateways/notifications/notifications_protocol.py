from abc import abstractmethod
from typing import Dict, Protocol


class NotificationsManagerProtocol(Protocol):

    @abstractmethod
    async def send_email_notifications(self, data: Dict) -> None: ...
