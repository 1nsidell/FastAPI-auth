from typing import Tuple

from auth.app.exceptions.auth import (
    IncorrectPasswordException,
    UserBlockedException,
)
from auth.app.exceptions.users import (
    UserAlreadyExistException,
    UserNotFoundException,
)
from auth.app.gateways import UsersManagementGatewayProtocol
from auth.app.providers import JWTProviderProtocol, PassProviderProtocol
from auth.app.repositories import UsersSQLRepositoryProtocol
from auth.app.schemas.users import SInfoUser
from auth.app.services import AuthServiceProtocol
from auth.core.db import SQLRepositoryUOW
from auth.core.schemas import SBaseSignIn, SBaseSignUp, TokenInfo


class AuthServiceImpl(AuthServiceProtocol):
    def __init__(
        self,
        users_sql_repository: UsersSQLRepositoryProtocol,
        users_management_gateway: UsersManagementGatewayProtocol,
        pass_provider: PassProviderProtocol,
        jwt_provider: JWTProviderProtocol,
        uow: SQLRepositoryUOW,
    ):
        self.users_sql_repository = users_sql_repository
        self.users_management_gateway = users_management_gateway
        self.pass_provider = pass_provider
        self.jwt_provider = jwt_provider
        self.uow = uow

    async def register_user(
        self, data: SBaseSignUp
    ) -> Tuple[TokenInfo, SInfoUser]:
        async with self.uow as session:
            if await self.users_sql_repository.get_user(
                session, email=data.email
            ):
                raise UserAlreadyExistException()
            hash_password = self.pass_provider.get_hash_password(data.password)
            user_id = await self.users_sql_repository.create_user(
                session,
                email=data.email,
                hash_password=hash_password,
            )
            user_info = await self.users_management_gateway.create_user_info(
                user_id=user_id,
                nickname=data.nickname,
            )
        user_session = self.jwt_provider.create_session(user_info)
        return user_session, user_info

    async def authenticate_user(self, data: SBaseSignIn) -> TokenInfo:
        async with self.uow as session:
            user = await self.users_sql_repository.get_user(
                session, email=data.email
            )
        if not user:
            raise UserNotFoundException()
        if not self.pass_provider.check_hash_password(
            data.password, user.hash_password
        ):
            raise IncorrectPasswordException()
        user_info = await self.users_management_gateway.get_user_info(user.id)
        if not user_info.is_active:
            raise UserBlockedException()
        user_session = self.jwt_provider.create_session(user_info)
        return user_session
