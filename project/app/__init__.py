import contextlib

import httpx
from fastapi import FastAPI

from app.redis import init_redis_pool
from app.routers.health import router as health_router
from app.routers.repositories import router as repositories_router

API_PREFIX = "/api"


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient() as http_client:
        yield {"http_client": http_client, "redis_client": init_redis_pool()}


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
    app.include_router(health_router, prefix=API_PREFIX)
    app.include_router(repositories_router, prefix=API_PREFIX)
    return app
