from dataclasses import dataclass

from app.github_client import GithubClient
from app.utils import build_pagination_links


@dataclass(frozen=True)
class RequestUrlMetadata:
    scheme: str
    netloc: str
    path: str


class RepositoriesService:
    def __init__(
        self, github_client: GithubClient, request_url_metadata: RequestUrlMetadata
    ):
        self._github_client = github_client
        self._base_url = (
            f"{request_url_metadata.scheme}://"
            f"{request_url_metadata.netloc}{request_url_metadata.path}"
        )

    async def get_repositories(
        self,
        per_page: str,
        page: int | None,
        q: str | None,
    ) -> dict:
        payload, headers = await self._github_client.get_repositories(per_page, page, q)
        link_header: str | None = headers.get("link")
        if link_header:
            pagination = build_pagination_links(link_header, self._base_url)
        else:
            pagination = {"prev": None, "next": None}

        payload.update({"pagination": pagination})
        return payload
