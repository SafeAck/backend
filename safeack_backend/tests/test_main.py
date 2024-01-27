from httpx import Response
from . import client


def test_200_root():
    res: Response = client.get("/")
    assert res.status_code == 200


def test_404_root():
    res: Response = client.get("/")
    assert res.status_code != 404
