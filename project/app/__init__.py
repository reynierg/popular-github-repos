import contextlib

import httpx
from fastapi import FastAPI

from app.routers.health import router as health_router
from app.routers.repositories import router as repositories_router


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient() as client:
        yield {"http_client": client}


def create_app() -> FastAPI:
    app = FastAPI(
        title="PopularGithubReposService",
        version="0.0.1",
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
        lifespan=lifespan,
    )
    app.include_router(health_router, prefix="/api")
    app.include_router(repositories_router, prefix="/repositories")
    return app
