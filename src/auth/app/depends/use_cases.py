from typing import Annotated

from fastapi import Depends

from auth.app.depends import AuthService, NotificationsService
from auth.app.use_cases import AuthUseCaseProtocol
from auth.app.use_cases.impls.auth import AuthUseCaseImpls


def get_auth_use_case(
    auth_service: AuthService,
    notifications_service: NotificationsService,
) -> AuthUseCaseProtocol:
    return AuthUseCaseImpls(
        auth_service=auth_service,
        notifications_service=notifications_service,
    )


AuthUseCase = Annotated[AuthUseCaseProtocol, Depends(get_auth_use_case)]
