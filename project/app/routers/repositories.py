import typing as t

from fastapi import APIRouter, Depends, Query, Request

from app.dependencies import get_github_client
from app.github_client import GithubClient
from app.schemas import RepositorySummaryListSchema
from app.utils import build_pagination_links

router = APIRouter(prefix="/repositories", tags=["Repositories"])


@router.get(
    "",
    response_model=RepositorySummaryListSchema,
    name="repositories:search-repositories",
)
async def search_repositories(
    request: Request,
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
    from_date: t.Annotated[
        str,
        Query(
            title="Lower bound date",
            description="Lower bound date for returned repositories",
            regex=r"^\d{4}-\d{2}-\d{2}$",
        ),
    ] = None,
    language: t.Annotated[
        str,
        Query(
            title="Language of the repositories",
            description="Language of the repositories to be returned",
        ),
    ] = None,
    github_client: GithubClient = Depends(get_github_client),
) -> dict:
    payload, headers = await github_client.get_repositories(
        per_page, page, from_date, language
    )
    link_header: str | None = headers.get("link")
    if link_header:
        base_url = f"{request.url.scheme}://{request.url.netloc}{request.url.path}"
        pagination = build_pagination_links(link_header, base_url)
    else:
        pagination = {"prev": None, "next": None}

    payload.update({"pagination": pagination})
    return payload
