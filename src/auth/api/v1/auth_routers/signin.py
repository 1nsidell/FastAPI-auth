from fastapi import APIRouter

from auth.app.depends import AuthUseCase
from auth.core.schemas import SBaseSignUp, TokenInfo
from auth.settings import settings

router = APIRouter()


@router.post(
    path=settings.api.signin, response_model=TokenInfo, status_code=200
)
async def signin(
    auth_use_case: AuthUseCase,
    data: SBaseSignUp,
) -> TokenInfo:
    return await auth_use_case.signin(data)
