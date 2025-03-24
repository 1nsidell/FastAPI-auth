from abc import abstractmethod
from datetime import timedelta
from typing import Any, Dict, List, Protocol

from auth.app.schemas.users import SInfoUser, SUser
from auth.core.schemas import TokenInfo


class JWTProviderProtocol(Protocol):
    TOKEN_TYPE_FIELD: str
    ACCESS_TOKEN_TYPE: str
    REFRESH_TOKEN_TYPE: str

    @abstractmethod
    def encode_jwt(
        self,
        payload: Dict,
        private_key: str,
        alghoritm: str,
        expire_minutes: int,
        expire_timedelta: timedelta | None,
    ) -> str: ...

    @abstractmethod
    def decode_jwt(
        self,
        token: str | bytes,
        public_key: str,
        algorithms: List[str],
    ) -> Dict[str, Any]: ...

    @abstractmethod
    def create_jwt(
        self,
        token_type: str,
        token_data: Dict,
        expire_minutes: int,
        expire_timedelta: timedelta | None,
    ) -> str: ...

    @abstractmethod
    def create_access_token(self, user_info: SInfoUser, time: int) -> str: ...

    @abstractmethod
    def create_refresh_token(self, user_info: SInfoUser) -> str: ...

    @abstractmethod
    def verification_token(self, token: str) -> Dict: ...

    @abstractmethod
    def verification_access_token(self, token: str) -> Dict: ...

    @abstractmethod
    def verification_refresh_token(self, refresh_token: str) -> int: ...

    @abstractmethod
    def create_session(self, user_info: SInfoUser) -> TokenInfo: ...
