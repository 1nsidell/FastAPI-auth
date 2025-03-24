import logging
from typing import Any, Self

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.app.models import Role, User
from auth.app.repositories import (
    UsersSQLRepositoryProtocol,
    handle_sql_exceptions,
)
from auth.app.schemas.users import SUser

log = logging.getLogger(__name__)


class UsersSQLRepositoryImpl(UsersSQLRepositoryProtocol):
    USER_MODEL = User
    ROLE_MODEL = Role

    @handle_sql_exceptions
    async def get_user(
        self: Self,
        session: AsyncSession,
        **filetr_by: Any,
    ) -> SUser:
        log.debug("Request user information.")
        stmt = (
            select(
                self.USER_MODEL.id,
                self.USER_MODEL.email,
                self.ROLE_MODEL.role,
                self.USER_MODEL.hash_password,
            )
            .filter_by(**filetr_by)
            .join(
                self.ROLE_MODEL,
                self.ROLE_MODEL.role_id == self.USER_MODEL.role_id,
            )
        )
        result = await session.execute(stmt)
        user_orm = result.scalar_one_or_none()
        if not user_orm:
            return None
        user = SUser.model_validate(user, from_attributes=True)
        log.debug("User successfully found with ID: %s.", user.id)
        return user

    @handle_sql_exceptions
    async def create_user(
        self: Self,
        session: AsyncSession,
        **data: Any,
    ) -> int:
        log.debug("Adding new user.")
        stmt = (
            insert(self.USER_MODEL).values(data).returning(self.USER_MODEL.id)
        )
        result = await session.execute(stmt)
        user_id = result.scalar()
        log.info("User successfully added with ID: %s.", result)
        return user_id

    @handle_sql_exceptions
    async def update_user(
        self: Self,
        session: AsyncSession,
        user_id: int,
        **values,
    ) -> None:
        log.info("User data update: %s.", user_id)
        stmt = (
            update(self.USER_MODEL)
            .where(self.USER_MODEL.id == user_id)
            .values(**values)
        )
        await session.execute(stmt)
        log.info("Successful update user with ID: %s.", user_id)

    @handle_sql_exceptions
    async def delete_user(
        self: Self,
        session: AsyncSession,
        user_id: int,
    ) -> None:
        log.info("User data delete: %s.", user_id)
        stmt = delete(self.USER_MODEL).where(self.USER_MODEL.id == user_id)
        await session.execute(stmt)
        log.info("Successful delete user with ID: %s.", user_id)
