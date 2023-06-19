import httpx
import pytest

from app.github_client import GithubClient


@pytest.mark.asyncio
async def test_github_client_should_return_10_repos_of_python_language(httpx_mock, repositories_factory):
    amount = 10
    language = "Python"

    expected_repositories_data = repositories_factory(amounts=amount)
    for repo in expected_repositories_data["items"]:
        repo["language"] = language

    expected_repositories_data["items"].sort(key=lambda x: x['stargazers_count'], reverse=True)

    async with httpx.AsyncClient() as http_client:
        gh_client = GithubClient(http_client)
        url = f"{gh_client.base_search_url}&per_page={amount}&q=language:{language}"
        httpx_mock.add_response(url=url, json=expected_repositories_data)
        response_payload = await gh_client.get_repositories(f"{amount}", None, language)

    assert response_payload == expected_repositories_data
