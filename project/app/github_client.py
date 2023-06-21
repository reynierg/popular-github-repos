import typing as t

from httpx import AsyncClient


class GithubClient:
    def __init__(self, async_client: AsyncClient):
        self._async_client = async_client
        self._base_search_url = "https://api.github.com/search/repositories"
        self._default_language = "Python"
        # GitHub's search API, configurable MAX page's size is 100 records.
        self._max_allowed_page_size = 100
        # GitHub's search API, default page's size is 30 records.
        self._default_page_size = 30

    @property
    def base_search_url(self):
        return self._base_search_url

    async def get_repositories(
        self,
        per_page: str,
        page: int | None,
        from_date: str | None,
        language: str | None,
    ) -> t.Tuple[dict, dict]:
        """
        Retrieves from the GitHub's API a page of repositories, with per_page records.
        According to the requirements, it is ONLY allowed, to specify to retrieve 10 OR 30 OR 50 repositories per page.
        """
        page_size = int(per_page)
        if page_size > self._default_page_size:
            # The API is being called to retrieve more than the 30 repositories per page,
            # that are returned at most by default, from the GitHub's search API, with every call.
            # Enforce that 30 < page_size <= 100:
            page_size = min(page_size, self._max_allowed_page_size)
        else:
            # Enforce that:
            # 1 <= page_size <= 30:
            page_size = max(1, page_size)

        params = {"sort": "stars", "order": "desc", "per_page": page_size}

        if page is not None:
            params["page"] = page

        # If no programming language was specified, "Python" will be used as default language:
        language_filter = (
            f"language:{language if language is not None else self._default_language}"
        )
        params[
            "q"
        ] = f"{language_filter}{f'+created:>{from_date}' if from_date else ''}"

        response = await self._async_client.get(self._base_search_url, params=params)
        response.raise_for_status()
        return response.json(), dict(response.headers)
