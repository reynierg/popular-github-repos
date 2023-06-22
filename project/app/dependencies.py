from functools import lru_cache

from fastapi import Depends, Request

from app.config import Settings
from app.github_client import GithubClient
from app.redis_client import RedisClient
from app.repositories_service import RepositoriesService, RequestUrlMetadata


@lru_cache
def get_settings() -> Settings:
    return Settings()


async def get_github_client(request: Request) -> GithubClient:
    return GithubClient(request.state.http_client)


async def get_redis_client(request: Request) -> RedisClient:
    return RedisClient(request.state.redis_client, get_settings().repos_page_ex)


async def get_repositories_service(
    request: Request,
    github_client: GithubClient = Depends(get_github_client),
    redis_client: RedisClient = Depends(get_redis_client),
) -> RepositoriesService:
    req_url_metadata = RequestUrlMetadata(
        request.url.scheme, request.url.netloc, request.url.path
    )
    return RepositoriesService(github_client, req_url_metadata, redis_client)
