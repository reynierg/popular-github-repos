import pytest
from fastapi.testclient import TestClient

from app import create_app
from app.config import Settings
from app.dependencies import get_settings


def get_settings_override() -> Settings:
    return Settings(testing=True)


@pytest.fixture(scope="module")
def http_client():
    """
    Setting-up a TestClient with the app to be re-used by tests that invoke the API endpoints.
    """
    app = create_app()
    # Override get_settings Dependency for running tests:
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down
