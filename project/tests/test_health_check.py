from fastapi import status

from app.config import EnvironmentEnum


def test_health_check(http_client):
    """
    GIVEN
    WHEN health check endpoint is called with GET method
    THEN response with status 200 and body OK is returned
    """
    response = http_client.get("/api/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"environment": EnvironmentEnum.dev, "testing": True, "health": True}
