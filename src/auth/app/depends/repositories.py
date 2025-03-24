from typing import Annotated

from fastapi import Depends

from auth.app.repositories import UsersSQLRepositoryProtocol
from auth.app.repositories.impls.users_sql import UsersSQLRepositoryImpl


def get_user_sql_repository() -> UsersSQLRepositoryProtocol:
    return UsersSQLRepositoryImpl()


UsersSQLRepository = Annotated[
    UsersSQLRepositoryProtocol, Depends(get_user_sql_repository)
]
