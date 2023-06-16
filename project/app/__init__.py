from fastapi import FastAPI

from app.routers.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="PopularGithubReposService",
        version="0.0.1",
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
    )
    app.include_router(health_router, prefix="/api")
    return app
