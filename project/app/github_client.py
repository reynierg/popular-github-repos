import typing as t

from httpx import AsyncClient, Response

from app.utils import build_pagination_links


class GithubClient:
    DEFAULT_CODING_LANGUAGE = "Python"
    # GitHub's search API, configurable MAX page's size is 100 records.
    MAX_ALLOWED_PAGE_SIZE = 100
    # GitHub's search API, default page's size is 30 records.
    DEFAULT_PAGE_SIZE = 30
    BASE_GITHUB_SEARCH_REPOSITORIES_URL = "https://api.github.com/search/repositories"
    REPOS_SORT_FIELD = "stars"
    REPOS_SORT_DIRECTION = "desc"
    REPOS_DEFAULT_PAGE_NUMBER = 1
    REPOS_DEFAULT_Q = f"language:{DEFAULT_CODING_LANGUAGE}"

    def __init__(self, async_client: AsyncClient):
        self._async_client = async_client

    def _build_get_repositories_params(
        self, per_page: str, page: int | None, q: str | None
    ):
        page_size = int(per_page)
        if page_size > self.DEFAULT_PAGE_SIZE:
            # The API is being called to retrieve more than the 30 repositories per page,
            # that are returned at most by default, from the GitHub's search API, with every call.
            # Enforce that 30 < page_size <= 100:
            page_size = min(page_size, self.MAX_ALLOWED_PAGE_SIZE)
        else:
            # Enforce that 1 <= page_size <= 30:
            page_size = max(1, page_size)

        # If no "q" parameter was received, we will query for repositories with "Python" as programming language:
        return {
            "sort": self.REPOS_SORT_FIELD,
            "order": self.REPOS_SORT_DIRECTION,
            "per_page": page_size,
            "page": page or self.REPOS_DEFAULT_PAGE_NUMBER,
            "q": q or self.REPOS_DEFAULT_Q,
        }

    @staticmethod
    def _explode_get_repositories_response(
        response: Response, svc_base_url: str
    ) -> t.Tuple[dict, str]:
        link_header: str | None = response.headers.get("link")
        if link_header:
            pagination = build_pagination_links(link_header, svc_base_url)
        else:
            pagination = {"prev": None, "next": None}

        payload = response.json()
        payload.update({"pagination": pagination})
        return payload, str(response.url)

    def build_url(
        self, per_page: str, page: int | None, q: str | None, method: str = "GET"
    ) -> str:
        params = self._build_get_repositories_params(per_page, page, q)
        request = self._async_client.build_request(
            method, self.BASE_GITHUB_SEARCH_REPOSITORIES_URL, params=params
        )
        return str(request.url)

    async def get_repositories(
        self, svc_base_url: str, per_page: str, page: int | None, q: str | None
    ) -> t.Tuple[dict, str]:
        """
        Retrieves from the GitHub's API a page of repositories, with per_page records.
        According to the requirements, it is ONLY allowed, to specify to retrieve 10 OR 30 OR 50 repositories per page.
        """
        params = self._build_get_repositories_params(per_page, page, q)
        response = await self._async_client.get(
            self.BASE_GITHUB_SEARCH_REPOSITORIES_URL, params=params
        )
        response.raise_for_status()
        return self._explode_get_repositories_response(response, svc_base_url)

    async def get_repositories_given_url(
        self, svc_base_url: str, url: str
    ) -> t.Tuple[dict, str]:
        response = await self._async_client.get(url)
        response.raise_for_status()
        return self._explode_get_repositories_response(response, svc_base_url)
