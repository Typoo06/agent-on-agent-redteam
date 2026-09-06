from fastapi.testclient import TestClient

from app.main import app


def test_openapi_contains_core_paths() -> None:
    client = TestClient(app)

    response = client.get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/health" in paths
    assert "/campaigns" in paths
    assert "/campaigns/{campaign_id}/runs" in paths
    assert "/runs/{run_id}/cancel" in paths
    assert "/targets/{target_id}/validate-scope" in paths
