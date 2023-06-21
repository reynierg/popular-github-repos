import typing as t

from httpx import AsyncClient


class GithubClient:
    DEFAULT_CODING_LANGUAGE = "Python"
    # GitHub's search API, configurable MAX page's size is 100 records.
    MAX_ALLOWED_PAGE_SIZE = 100
    # GitHub's search API, default page's size is 30 records.
    DEFAULT_PAGE_SIZE = 30
    BASE_SEARCH_URL = "https://api.github.com/search/repositories"

    def __init__(self, async_client: AsyncClient):
        self._async_client = async_client

    async def get_repositories(
        self, per_page: str, page: int | None, q: str | None
    ) -> t.Tuple[dict, dict]:
        """
        Retrieves from the GitHub's API a page of repositories, with per_page records.
        According to the requirements, it is ONLY allowed, to specify to retrieve 10 OR 30 OR 50 repositories per page.
        """
        page_size = int(per_page)
        if page_size > self.DEFAULT_PAGE_SIZE:
            # The API is being called to retrieve more than the 30 repositories per page,
            # that are returned at most by default, from the GitHub's search API, with every call.
            # Enforce that 30 < page_size <= 100:
            page_size = min(page_size, self.MAX_ALLOWED_PAGE_SIZE)
        else:
            # Enforce that 1 <= page_size <= 30:
            page_size = max(1, page_size)

        params = {"sort": "stars", "order": "desc", "per_page": page_size}
        if page is not None:
            params["page"] = page

        # If no "q" parameter was received, we will query for repositories with "Python" as programming language:
        q = q or f"language:{self.DEFAULT_CODING_LANGUAGE}"
        params["q"] = q

        response = await self._async_client.get(self.BASE_SEARCH_URL, params=params)
        response.raise_for_status()
        return response.json(), dict(response.headers)
