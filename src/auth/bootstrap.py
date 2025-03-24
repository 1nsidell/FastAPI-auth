from contextlib import asynccontextmanager

from fastapi import FastAPI

from auth.app.depends import RMQManager, UsersManagementClientManager
from auth.core import SQLDBHelper
from auth.core.loggers import setup_logging
from auth.exceptions import apply_exceptions_handlers
from auth.middlewares import apply_middlewares
from auth.routers import apply_routes
from auth.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Pre-initialization of the application.
    """
    # startup
    setup_logging(settings)
    SQLDBHelper.startup()
    UsersManagementClientManager.startup()
    await RMQManager.startup()
    yield
    # shutdown
    await SQLDBHelper.shutdown()
    await UsersManagementClientManager.shutdown()
    await RMQManager.shutdown()


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        docs_url="/docs",
        openapi_url="/docs.json",
    )
    return apply_exceptions_handlers(apply_routes(apply_middlewares(app)))
