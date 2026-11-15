
from sqlalchemy.exc import OperationalError


def test_health_endpoint(client):
    response = client.get("/api/health/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["application"] == "Cloud Incident Manager"


def test_database_health(client):
    response = client.get("/api/health/database")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "connected"
    assert data["database"] == "available"


def test_database_health_returns_503_when_database_unavailable(client):
    from app.routes import health

    class BrokenConnection:
        def __enter__(self):
            raise OperationalError(
                "SELECT 1",
                {},
                Exception("Simulated database connection failure"),
            )

        def __exit__(self, exc_type, exc_value, traceback):
            return False

    class BrokenEngine:
        def connect(self):
            return BrokenConnection()

    client.app.dependency_overrides[health.get_engine] = (
        lambda: BrokenEngine()
    )

    response = client.get("/api/health/database")

    assert response.status_code == 503
    assert response.json()["detail"]["database"] == "unavailable"
