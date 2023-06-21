import httpx
import pytest

from app.github_client import GithubClient


@pytest.mark.asyncio
async def test_github_client_should_return_10_repos_with_python_language(httpx_mock, repositories_factory):
    per_page = 10
    language = "Python"

    expected_repositories_data = repositories_factory(amounts=per_page)
    for repo in expected_repositories_data["items"]:
        repo["language"] = language

    expected_repositories_data["items"].sort(key=lambda x: x['stargazers_count'], reverse=True)

    async with httpx.AsyncClient() as http_client:
        gh_client = GithubClient(http_client)
        url = f"{gh_client.base_search_url}?sort=stars&order=desc&per_page={per_page}&q=language:{language}"
        httpx_mock.add_response(url=url, json=expected_repositories_data)
        response_payload, _ = await gh_client.get_repositories(f"{per_page}", None, None, language)

    assert response_payload == expected_repositories_data
