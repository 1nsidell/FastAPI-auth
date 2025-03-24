from fastapi import APIRouter

from auth.api.v1 import signin_router, signup_router
from auth.settings import settings

v1_router = APIRouter(
    prefix=settings.api.v1_prefix,
    tags=["USERS-AUTH-V1"],
)

v1_sub_routers = (
    signin_router,
    signup_router,
)

for router in v1_sub_routers:
    v1_router.include_router(router)
