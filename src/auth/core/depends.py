"""Module core IOC container."""

from __future__ import annotations
from typing import Annotated, Callable, TYPE_CHECKING

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.core import SQLDatabaseHelper, SQLRepositoryUOW
from auth.settings import get_settings, settings

if TYPE_CHECKING:
    from auth.settings import Settings


# Depends Settings instance
SettingsService = Annotated["Settings", Depends(get_settings)]


def get_sql_db_helper(settings: Settings) -> SQLDatabaseHelper:
    """Create an singleton instance of DB helper."""
    return SQLDatabaseHelper(
        url=settings.db.url,
        echo=settings.db.ECHO,
        echo_pool=settings.db.ECHO_POOL,
        pool_size=settings.db.POOL_SIZE,
        max_overflow=settings.db.MAX_OVERFLOW,
    )


# Singleton DBHelper instance
SQLDBHelper: SQLDatabaseHelper = get_sql_db_helper(settings)


def get_async_session_factory() -> Callable[[], AsyncSession]:
    """Getting async session factory for Depends object."""
    return SQLDBHelper.async_session_factory


AsyncSessionFactory = Annotated[
    Callable[[], AsyncSession], Depends(get_async_session_factory)
]


def get_uow(
    async_session_factory: AsyncSessionFactory,
) -> SQLRepositoryUOW:
    """Create a Depends instance of uow."""
    return SQLRepositoryUOW(async_session_factory)


UoW = Annotated[SQLRepositoryUOW, Depends(get_uow)]
