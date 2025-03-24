import uvicorn

from auth.bootstrap import create_app
from auth.settings import settings

app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        host=settings.run.host,
        port=settings.run.port,
    )
