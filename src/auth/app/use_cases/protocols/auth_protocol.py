from abc import abstractmethod
from typing import Protocol

from auth.app.services import AuthServiceProtocol, NotificationsServiceProtocol
from auth.core.schemas import SBaseSignIn, SBaseSignUp, TokenInfo


class AuthUseCaseProtocol(Protocol):

    auth_service: AuthServiceProtocol
    notifications_service: NotificationsServiceProtocol

    @abstractmethod
    async def signup(self, data: SBaseSignUp) -> TokenInfo: ...

    @abstractmethod
    async def signin(self, data: SBaseSignIn) -> TokenInfo: ...
