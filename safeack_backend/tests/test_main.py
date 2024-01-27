from safeack_backend.api import app
from fastapi.testclient import TestClient
from httpx import Response

client = TestClient(app)


def test_200_root():
    res: Response = client.get("/")
    assert res.status_code == 200


def test_404_root():
    res: Response = client.get("/")
    assert res.status_code != 404
