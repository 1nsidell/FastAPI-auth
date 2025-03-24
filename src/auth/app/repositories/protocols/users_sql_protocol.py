"""
A protocol describing the methods and attributes of a repository,
that must be defined for the application to work
"""

import logging
from abc import abstractmethod
from typing import Any, Protocol, Self

from sqlalchemy.ext.asyncio import AsyncSession

from auth.app.schemas.users import SUser

log = logging.getLogger("repositories")


class UsersSQLRepositoryProtocol(Protocol):

    @abstractmethod
    async def get_user(
        self: Self,
        session: AsyncSession,
        **filetr_by: Any,
    ) -> SUser:
        """Get information about the user.

        Args:
            session (AsyncSession): transaction session.
            **filetr_by (Any): argument to search for user data.

        Returns:
            SUser: user data.
        """
        ...

    @abstractmethod
    async def create_user(
        self: Self,
        session: AsyncSession,
        **data: Any,
    ) -> int:
        """Add a new user.

        Args:
            session (AsyncSession): transaction session.
            data (Any): registered user data.

        Returns:
            int: newly registered user id.
        """
        ...

    @abstractmethod
    async def update_user(
        self: Self,
        session: AsyncSession,
        user_id: int,
        **data: Any,
    ) -> None:
        """Update user information by user ID.

        Args:
            session (AsyncSession): transaction session.
            user_id (int): user id.
        """
        ...

    @abstractmethod
    async def delete_user(
        self: Self,
        session: AsyncSession,
        user_id: int,
    ) -> None:
        """Deleting a user account by ID.

        Args:
            session (AsyncSession): transaction session.
            user_id (int): user id.
        """
        ...
