def test_create_incident(client):
    response = client.post(
        "/api/incidents/",
        json={
            "title": "EC2 instance unavailable",
            "description": "Application server stopped responding",
            "severity": "High",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "EC2 instance unavailable"
    assert data["severity"] == "High"
    assert data["status"] == "Open"


def test_invalid_severity(client):
    response = client.post(
        "/api/incidents/",
        json={
            "title": "Test incident",
            "description": "Testing invalid severity",
            "severity": "Extreme",
        },
    )

    assert response.status_code == 400
