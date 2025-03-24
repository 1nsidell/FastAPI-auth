import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import jwt

from auth.app.exceptions.jwt import InvalidTokenException, TokenTimeOutException
from auth.app.providers import JWTProviderProtocol
from auth.app.schemas.users import SInfoUser
from auth.core.schemas import TokenInfo
from auth.settings import settings

log = logging.getLogger("app")


class JWTProviderImpl(JWTProviderProtocol):
    TOKEN_TYPE_FIELD = "type"
    ACCESS_TOKEN_TYPE = "access"
    REFRESH_TOKEN_TYPE = "refresh"

    def encode_jwt(
        self,
        payload: Dict,
        private_key: str = settings.auth_jwt.PRIVATE_KEY_PATH.read_text(),
        alghoritm: str = settings.auth_jwt.ENCODE_ALGORITHM,
        expire_minutes: int = settings.auth_jwt.ACCESS_EXPIRE_MINUTES,
        expire_timedelta: Optional[timedelta] = None,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.now(timezone.utc)

        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)

        to_encode.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(to_encode, private_key, algorithm=alghoritm)
        log.debug("JWT encoded.")
        return encoded

    def decode_jwt(
        self,
        token: str | bytes,
        public_key: str = settings.auth_jwt.PUBLIC_KEY_PATH.read_text(),
        algorithms: List[str] = settings.auth_jwt.DECODE_ALGORITHMS,
    ) -> Dict[str, Any]:
        decoded = jwt.decode(token, public_key, algorithms=algorithms)
        log.debug("JWT decoded.")
        return decoded

    def create_jwt(
        self,
        token_type: str,
        token_data: Dict,
        expire_minutes: int = settings.auth_jwt.ACCESS_EXPIRE_MINUTES,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        jwt_payload = {self.TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(token_data)

        log.debug("Creating JWT with type: %s.", token_type)
        return self.encode_jwt(
            payload=jwt_payload,
            expire_minutes=expire_minutes,
            expire_timedelta=expire_timedelta,
        )

    def create_access_token(
        self,
        user_info: SInfoUser,
        time: int,
    ) -> str:
        jwt_payload = {
            "sub": user_info.user_id,
            "is_verified": user_info.is_verified,
            "nickname": user_info.nickname,
            "avatar": user_info.avatar,
        }
        log.debug("Creating access token for user: %s.", user_info.user_id)
        return self.create_jwt(self.ACCESS_TOKEN_TYPE, jwt_payload, time)

    def create_refresh_token(self, user_info: SInfoUser) -> str:
        jwt_payload = {
            "sub": user_info.user_id,
        }
        log.debug("Creating refresh token for user: %s.", user_info.user_id)
        return self.create_jwt(
            self.REFRESH_TOKEN_TYPE,
            jwt_payload,
            expire_timedelta=timedelta(
                days=settings.auth_jwt.REFRESH_EXPIRE_DAYS
            ),
        )

    def verification_token(self, token: str) -> Dict:
        try:
            payload = self.decode_jwt(token)
            log.debug("Verification token was successful.")
        except jwt.PyJWTError as e:
            log.exception("Token verification error.")
            raise InvalidTokenException(e)
        expire = payload.get("exp")
        if (not expire) or (int(expire)) < datetime.now(
            timezone.utc
        ).timestamp():
            log.warning("Token expired user: %s.", payload.get("sub"))
            raise TokenTimeOutException()
        return payload

    def verification_access_token(self, token: str) -> Dict:
        log.debug("Verification access token has begun.")
        payload = self.verification_token(token)
        token_type = payload.get(self.TOKEN_TYPE_FIELD)
        if token_type != self.ACCESS_TOKEN_TYPE:
            log.warning("Invalid access token user: %s.", payload.get("sub"))
            raise InvalidTokenException()
        log.debug("Verification access token successful.")
        return payload

    def verification_refresh_token(self, refresh_token: str) -> int:
        log.debug("Verification refresh token has begun.")
        payload = self.verification_token(refresh_token)
        token_type = payload.get(self.TOKEN_TYPE_FIELD)
        if token_type != self.REFRESH_TOKEN_TYPE:
            log.warning("Invalid refresh token user: %s.", payload.get("sub"))
            raise InvalidTokenException()
        log.debug("Verification refresh token successful.")
        return payload["sub"]

    def create_session(self, user_info: SInfoUser) -> TokenInfo:
        log.debug("Create session for user: %s.", user_info.user_id)
        access_token = self.create_access_token(
            user_info, settings.auth_jwt.ACCESS_EXPIRE_MINUTES
        )
        refresh_token = self.create_refresh_token(user_info)
        log.debug("Session successfully created.")
        return TokenInfo(access_token=access_token, refresh_token=refresh_token)
