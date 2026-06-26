from app import create_app


def test_health_endpoint():
    client = create_app().test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_jobs_endpoint():
    client = create_app().test_client()
    response = client.get("/api/jobs")
    assert response.status_code == 200
