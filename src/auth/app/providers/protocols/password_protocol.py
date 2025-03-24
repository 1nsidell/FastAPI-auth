from abc import abstractmethod
from typing import Protocol


class PassProviderProtocol(Protocol):
    @abstractmethod
    def get_hash_password(cls, password: str) -> bytes: ...

    @abstractmethod
    def check_hash_password(
        cls, password: str, hashed_password: bytes
    ) -> bool: ...
