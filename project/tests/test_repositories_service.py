import typing as t

from fastapi import Request, status

from app.dependencies import get_github_client, get_redis_client


def test_should_retrieve_data_from_github_and_cache(http_client, repositories_factory):
    """
    GIVEN the Redis cache client is mocked and will behave like if the GitHub repositories' data for the required URL
        isn't cached.
        The GitHub client is mocked to return a fixed amount of fake GitHub repositories.
    WHEN search repositories endpoint is called with GET method
    THEN response with status 200 and body with the fake GitHub repositories will be returned.
        The Redis cache client will be called to cache the fake GitHub repositories.
    """

    # Generate fake github repositories data. 10 in total:
    per_page = 10
    language = "Python"
    expected_repositories_data = repositories_factory(items=per_page)
    # All will have 'Python' as the language:
    for repo in expected_repositories_data["items"]:
        repo["language"] = language

    expected_repositories_data["items"].sort(key=lambda x: x['stargazers_count'], reverse=True)

    class MockRedisClient:
        def __init__(self):
            self.to_stored_in_cache: dict = None

        async def get_repositories(self, _: str) -> dict | None:
            return None

        async def cache_repositories(self, _: str, repositories_data: dict):
            self.to_stored_in_cache = repositories_data
            return None

    class MockGithubClient:
        def build_url(self, _: str, __: int | None, ___: str | None, ____: str = "GET") -> str:
            return ""

        async def get_repositories_given_url(self, _: str, __: str) -> t.Tuple[dict, str]:
            return expected_repositories_data, ""

    redis_client = MockRedisClient()

    def override_get_redis_client(_: Request):
        return redis_client

    def override_get_github_client(_: Request):
        return MockGithubClient()

    http_client.app.dependency_overrides[get_redis_client] = override_get_redis_client
    http_client.app.dependency_overrides[get_github_client] = override_get_github_client

    search_repos_url = http_client.app.url_path_for("repositories:search-repositories")
    response = http_client.get(f"{search_repos_url}?per_page={per_page}&q=language:{language}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_repositories_data

    # Verify that the RepositoriesService, after retrieve the repositories' data from MockGithubClient,
    # is using the MockRedisClient to cache the data:
    assert redis_client.to_stored_in_cache == expected_repositories_data
