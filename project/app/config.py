from enum import Enum

from pydantic import BaseSettings


class EnvironmentEnum(str, Enum):
    DEV = "dev"
    PROD = "prod"


class Settings(BaseSettings):
    environment: EnvironmentEnum = EnvironmentEnum.DEV
    testing: bool = False
