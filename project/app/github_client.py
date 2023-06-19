from io import StringIO

from httpx import AsyncClient


class GithubClient:
    def __init__(self, async_client: AsyncClient):
        self._async_client = async_client
        self._base_search_url = (
            "https://api.github.com/search/repositories?sort=stars&order=desc"
        )
        self._default_language = "Python"
        # GitHub's search API, configurable MAX page's size is 100 records.
        self._max_allowed_page_size = 100
        # GitHub's search API, default page's size is 30 records.
        self._default_page_size = 30

    @property
    def base_search_url(self):
        return self._base_search_url

    async def get_repositories(
        self, amount: str, from_date: str | None, language: str | None
    ):
        """
        Retrieves from the GitHub's API the amount of repositories specified.
        According to the requirements, it is ONLY allowed, to specify to retrieve 10 OR 30 OR 50 repositories.
        """
        url_string_io: StringIO = StringIO()
        url_string_io.write(self._base_search_url)

        required_amount = int(amount)
        if required_amount > self._default_page_size:
            # The API is being called to retrieve more than the 30 repositories, that are returned at most by default,
            # from the GitHub's search API, with every call.
            # This implies, that  30 < required_amount <= 100
            required_amount = min(required_amount, self._max_allowed_page_size)
        else:
            # 1 <= required_amount <= 30:
            required_amount = max(1, required_amount)

        # Adjust properly the "per_page" query's string, to get at most, the amount of repositories requested,
        # in a single call, from the GitHub's search API:
        url_string_io.write(f"&per_page={required_amount}")

        if from_date and language:
            url_string_io.write(f"&q=created:>={from_date}+language:{language}")
        elif from_date:
            url_string_io.write(f"&q=created:>={from_date}")
        elif language:
            url_string_io.write(f"&q=language:{language}")
        else:
            # If no programming language was specified, "Python" will be used as default language:
            url_string_io.write(f"&q=language:{self._default_language}")

        url: str = url_string_io.getvalue()
        response = await self._async_client.get(url)
        response.raise_for_status()
        return response.json()
