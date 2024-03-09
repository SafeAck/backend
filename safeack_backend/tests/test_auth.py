from httpx import Response
from . import client


def test_create_user():
    payload = {
        "email": "john.doe@example.com",
        "first_name": "John",
        "full_name": "John Doe",
        "last_name": "Doe",
        "password": "ExamPL3P4$$W0rD!!0194",
    }
    res: Response = client.post("/api/v1/auth/signup", json=payload)
    res_body = res.json()

    assert res.status_code == 200
    assert res_body == {"msg": "user signed up sucessfully"}


def test_unsuccessful_create_user():
    payloads = [
        {
            "email": "john.doe@example##%00.com",
            "first_name": "John",
            "full_name": "John Doe",
            "last_name": "Doe",
            "password": "ExamPL3P4$$W0rD!!0194",
        },
        {
            "email": "john.doe@example.com",
            "first_name": "John%00.test",
            "full_name": "John Doe",
            "last_name": "Doe",
            "password": "ExamPL3P4$$W0rD!!0194",
        },
        {
            "email": "john.doe@example.com",
            "first_name": "John",
            "full_name": "John Doe",
            "last_name": "Doe",
            "password": "",
        },
        {
            "email": "john.doe@example.com",
            "first_name": "<script>confirm(1)</script>",
            "full_name": "<script>confirm(2)</script>",
            "last_name": "<script>confirm(3)</script>",
            "password": "12tlskj@!kl",
        },
    ]
    for payload in payloads:
        res: Response = client.post("/api/v1/auth/signup", json=payload)

        res_body = res.json()

        assert res.status_code in {200, 400, 422}
        assert res_body != {"msg": "user signed up sucessfully"}


def test_login_user():
    payload = {"email": "john.doe@example.com", "password": "ExamPL3P4$$W0rD!!0194"}
    res: Response = client.post("/api/v1/auth/token", json=payload)

    res_body = res.json()
    token = res_body.get('access_token', "")

    assert res.status_code == 200
    assert token != ""
    assert token is not None


def test_oauth_login_user():
    payload = {
        "grant_type": "password",
        "scope": "me:read+me:write+me:read_results+me:write_results+staff:restricted_read",
        "username": "john.doe@example.com",
        "password": "ExamPL3P4$$W0rD!!0194",
    }

    res: Response = client.post("/api/v1/auth/oauth/login", data=payload)
    res_body = res.json()
    token = res_body.get('access_token', "")

    assert res.status_code == 200
    assert token != ""
    assert token is not None
