from enum import Enum

from pydantic import BaseSettings


class EnvironmentEnum(str, Enum):
    dev = 'dev'
    prod = 'prod'


class Settings(BaseSettings):
    environment: EnvironmentEnum = EnvironmentEnum.dev
    testing: bool = False
