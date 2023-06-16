from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.config import EnvironmentEnum, Settings
from app.dependencies import get_settings


class HealthSchema(BaseModel):
    health: bool = Field(title="The service's health status")
    environment: EnvironmentEnum = Field(title="The running environment")
    testing: bool = Field(title="If tests are being executed or not")


router = APIRouter(
    prefix="/health",
    tags=["HealthCheck"]
)


@router.get("", response_model=HealthSchema)
def health_check(settings: Settings = Depends(get_settings)) -> dict:
    return {
        "health": True,
        "environment": settings.environment,
        "testing": settings.testing
    }
