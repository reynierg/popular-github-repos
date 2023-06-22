import sys
import typing

if sys.version_info >= (3, 10):  # pragma: no cover
    from typing import ParamSpec
else:  # pragma: no cover
    from typing_extensions import ParamSpec

from dataclasses import dataclass

from app.github_client import GithubClient
from app.redis_client import RedisClient

P = ParamSpec("P")


class BackgroundTasksProtocol(typing.Protocol):
    def add_task(
        self, func: typing.Callable[P, typing.Any], *args: P.args, **kwargs: P.kwargs
    ) -> None:
        ...

    async def __call__(self) -> None:
        ...


@dataclass(frozen=True)
class RequestUrlMetadata:
    scheme: str
    netloc: str
    path: str


class RepositoriesService:
    def __init__(
        self,
        github_client: GithubClient,
        request_url_metadata: RequestUrlMetadata,
        redis_client: RedisClient,
    ):
        self._github_client = github_client
        self._base_url = (
            f"{request_url_metadata.scheme}://"
            f"{request_url_metadata.netloc}{request_url_metadata.path}"
        )
        self._redis_client = redis_client

    async def get_repositories(
        self,
        per_page: str,
        page: int | None,
        q: str | None,
        background_tasks: BackgroundTasksProtocol | None,
    ) -> dict:
        # First, try to retrieve the results from the Redis cache:
        github_endpoint_url = self._github_client.build_url(per_page, page, q)
        print(f"github_endpoint_url: {github_endpoint_url}")
        payload = await self._redis_client.get_repositories(github_endpoint_url)
        if payload:
            return payload

        payload, url = await self._github_client.get_repositories_given_url(
            self._base_url, github_endpoint_url
        )
        print(f"url: {url}")
        if background_tasks:
            background_tasks.add_task(
                self._redis_client.cache_repositories, url, payload
            )
        else:
            await self._redis_client.cache_repositories(url, payload)

        return payload
