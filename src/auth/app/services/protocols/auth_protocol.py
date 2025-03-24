from abc import abstractmethod
from typing import Protocol, Tuple

from auth.app.schemas.users import SInfoUser
from auth.core.schemas import SBaseSignIn, SBaseSignUp, TokenInfo


class AuthServiceProtocol(Protocol):

    @abstractmethod
    async def register_user(
        self, data: SBaseSignUp
    ) -> Tuple[TokenInfo, SInfoUser]: ...

    @abstractmethod
    async def authenticate_user(self, data: SBaseSignIn) -> TokenInfo: ...
