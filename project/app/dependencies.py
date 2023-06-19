from functools import lru_cache

from fastapi import Request

from app.config import Settings
from app.github_client import GithubClient


@lru_cache
def get_settings() -> Settings:
    return Settings()


async def get_github_client(request: Request) -> GithubClient:
    return GithubClient(request.state.http_client)
