from enum import Enum

from pydantic import BaseSettings


class EnvironmentEnum(str, Enum):
    DEV = "dev"
    PROD = "prod"


class Settings(BaseSettings):
    environment: EnvironmentEnum = EnvironmentEnum.DEV
    testing: bool = False
    redis_url: str = "redis://repos-redis-service:6379"
    repos_page_ex = 60 * 60 * 24  # 24h
