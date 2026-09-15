from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    """Test the /api/v1/health endpoint with standardized success response format."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["success"] is True
    assert "data" in res_json
    assert res_json["data"]["status"] == "ok"
    assert "version" in res_json["data"]
    assert "environment" in res_json["data"]
