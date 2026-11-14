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
