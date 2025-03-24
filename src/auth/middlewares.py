"""
Основной модуль для middleware приложения.
"""

from fastapi import FastAPI

from auth.core.middlewares.logger_middleware import RequestLoggingMiddleware

middlewares = (RequestLoggingMiddleware,)


def apply_middlewares(app: FastAPI) -> FastAPI:
    """
    Применяем middleware.
    """
    for middleware in middlewares:
        app.add_middleware(middleware)
    return app
