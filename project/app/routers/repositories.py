import typing as ty

from fastapi import APIRouter, Depends, Query

from app.dependencies import get_github_client
from app.github_client import GithubClient
from app.schemas import RepositorySummaryListSchema

router = APIRouter(prefix="/repositories", tags=["Repositories"])


@router.get(
    "",
    response_model=RepositorySummaryListSchema,
    name="repositories:search-repositories",
)
async def search_repositories(
    amount: ty.Annotated[
        str,
        Query(
            title="Amount of GitHub repositories",
            description="Amount of GitHub repositories to be returned",
            regex="^10|50|100$",
        ),
    ] = "10",
    from_date: ty.Annotated[
        str,
        Query(
            title="Lower bound date",
            description="Lower bound date for returned repositories",
            regex=r"^\d{4}-\d{2}-\d{2}$",
        ),
    ] = None,
    language: ty.Annotated[
        str,
        Query(
            title="Language of the repositories",
            description="Language of the repositories to be returned",
        ),
    ] = None,
    github_client: GithubClient = Depends(get_github_client),
) -> dict:
    return await github_client.get_repositories(amount, from_date, language)
