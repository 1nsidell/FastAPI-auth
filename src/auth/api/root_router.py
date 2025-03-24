from fastapi import APIRouter

from auth.api.health_check.healthcheck import healthcheck_router
from auth.api.v1.router import v1_router
from auth.settings import settings

root_router = APIRouter(prefix=settings.api.prefix)

root_sub_routers = (
    healthcheck_router,
    v1_router,
)

for router in root_sub_routers:
    root_router.include_router(router)
