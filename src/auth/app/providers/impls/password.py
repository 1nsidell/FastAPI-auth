import logging

import bcrypt

from auth.app.providers import PassProviderProtocol

log = logging.getLogger("app")


class PassProviderImpl(PassProviderProtocol):
    def get_hash_password(self, password: str) -> bytes:
        hashed: bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        log.debug("User password hashing.")
        return hashed

    def check_hash_password(
        self, password: str, hashed_password: bytes
    ) -> bool:
        result: bool = bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )
        log.debug("Check user password, result: %s.", result)
        return result
