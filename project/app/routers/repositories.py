import typing as t

from fastapi import APIRouter, Depends, Query

from app.dependencies import get_repositories_service
from app.repositories_service import RepositoriesService
from app.schemas import RepositorySummaryListSchema

router = APIRouter(prefix="/repositories", tags=["Repositories"])


@router.get(
    "",
    response_model=RepositorySummaryListSchema,
    name="repositories:search-repositories",
)
async def search_repositories(
    per_page: t.Annotated[
        str,
        Query(
            title="Results per page",
            description="Count of GitHub repositories to include per page",
            regex="^10|50|100$",
        ),
    ] = "10",
    page: t.Annotated[
        int,
        Query(
            title="Page index",
            description="Index of the page to fetch with repositories data",
        ),
    ] = None,
    q: t.Annotated[
        str,
        Query(
            title="Repositories query",
            description="Repositories query to be send to the GitHub's repositories search API",
        ),
    ] = None,
    repositories_service: RepositoriesService = Depends(get_repositories_service),
) -> dict:
    return await repositories_service.get_repositories(per_page, page, q)
