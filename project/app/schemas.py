from pydantic import BaseModel, Field


class OwnerSchema(BaseModel):
    id: int = Field(title="The owner's id")
    login: str = Field(title="The owner's login")
    type: str = Field(title="The owner's type")


class LicenseSchema(BaseModel):
    key: str = Field(title="The license's key")
    name: str = Field(title="The license's name")
    spdx_id: str = Field(title="The license's spdx_id")


class RepositorySummarySchema(BaseModel):
    id: int = Field(title="The repository's id")
    name: str = Field(title="The repository's name")
    full_name: str = Field(title="The repository's full_name")
    private: bool = Field(title="If the repository's is private or not")
    html_url: str = Field(title="The repository's html_url")
    description: str | None = Field(title="The repository's description")
    stargazers_count: str = Field(title="The repository's stars")
    language: str | None = Field(title="The repository's main language")
    owner: OwnerSchema | None = Field(title="The repository's owner")
    license: LicenseSchema | None = Field(title="The repository's license")


class RepositorySummaryListSchema(BaseModel):
    total_count: int = Field(title="The total count of repositories")
    incomplete_results: bool = Field(title="If the response is incomplete")
    items: list[RepositorySummarySchema] = Field(
        title="The data of the repositories in the response's payload"
    )
