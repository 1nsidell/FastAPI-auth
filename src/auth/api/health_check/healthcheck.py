from fastapi import APIRouter

from auth.api.health_check.liveness import router as liveness_router
from auth.settings import settings

healthcheck_router = APIRouter(
    prefix=settings.api.healthcheck,
    tags=["HEALTH-CHECK"],
)

healthcheck_router_sub_routers = (liveness_router,)

for router in healthcheck_router_sub_routers:
    healthcheck_router.include_router(router)
