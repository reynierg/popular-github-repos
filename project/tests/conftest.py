import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest_factoryboy import register

from app.config import Settings
from app.dependencies import get_settings
from tests.factories import RepositoriesFactory


def get_settings_override() -> Settings:
    return Settings(testing=True)


@pytest.fixture
def app() -> FastAPI:
    from app import create_app
    return create_app()


@pytest.fixture
def http_client(app):
    """
    Setting-up a TestClient with the app to be re-used by tests that invoke the API endpoints.
    """
    # Override get_settings Dependency for running tests:
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down


register(RepositoriesFactory)
