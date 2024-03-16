"""
Module for testing Authentication
"""

import pytest

from httpx import Response, AsyncClient
from . import (
    app,
    base_url,
    TestingSessionLocal,
    normal_user_email,
    normal_user_passwd,
    superuser_email,
    superuser_passwd,
)
from .utils import set_user_active, set_user_superuser


# This is the same as using the @pytest.mark.anyio on all test functions in the module
pytestmark = pytest.mark.anyio


async def test_create_user():
    """
    Creates user sign up creation functionality
    """
    payload = {
        "email": normal_user_email,
        "first_name": "John",
        "full_name": "John Doe",
        "last_name": "Doe",
        "password": normal_user_passwd,
    }

    async with AsyncClient(app=app, base_url=base_url) as ac:
        res: Response = await ac.post("/api/v1/auth/signup", json=payload)
        res_body = res.json()
        assert res.status_code == 200
        assert res_body == {"msg": "user signed up sucessfully"}

        # mark this newly created user active
        db = TestingSessionLocal()
        set_user_active(db, normal_user_email)
        db.close()


async def test_create_superuser():
    """
    Creates user sign up creation functionality
    """
    payload = {
        "email": superuser_email,
        "first_name": "Super",
        "last_name": "Doe",
        "full_name": "Super Doe",
        "password": superuser_passwd,
    }

    async with AsyncClient(app=app, base_url=base_url) as ac:
        res: Response = await ac.post("/api/v1/auth/signup", json=payload)
        res_body = res.json()

        assert res.status_code == 200
        assert res_body == {"msg": "user signed up sucessfully"}

        # mark this newly created user active
        db = TestingSessionLocal()
        set_user_superuser(db, superuser_email)
        db.close()


async def test_unsuccessful_create_user():
    """
    Tests user sign up functionality which should fail
    """
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
        async with AsyncClient(app=app, base_url=base_url) as ac:
            res: Response = await ac.post("/api/v1/auth/signup", json=payload)
            assert res.status_code in {200, 400, 422}
            assert res.json() != {"msg": "user signed up sucessfully"}


async def test_login_user():
    """
    Tests User Login functionality
    """
    # login user
    payload = {"email": "john.doe@example.com", "password": "ExamPL3P4$$W0rD!!0194"}
    async with AsyncClient(app=app, base_url=base_url) as ac:
        res: Response = await ac.post("/api/v1/auth/token", json=payload)
        res_body = res.json()
        token = res_body.get('access_token', "")

        assert res.status_code == 200
        assert token != ""
        assert token is not None


async def test_oauth_login_user():
    """
    Tests Oauth login functionality
    """
    payload = {
        "grant_type": "password",
        "scope": "me:read+me:write+me:read_results+me:write_results+staff:restricted_read",
        "username": "john.doe@example.com",
        "password": "ExamPL3P4$$W0rD!!0194",
    }

    async with AsyncClient(app=app, base_url=base_url) as ac:
        res: Response = await ac.post("/api/v1/auth/oauth/login", data=payload)
        res_body = res.json()
        token = res_body.get('access_token', "")

        assert res.status_code == 200
        assert token != ""
        assert token is not None


async def test_scanner_token_generation():
    """
    Test scanner token generation
    """
    login_payload = {"email": "john.doe@example.com", "password": "ExamPL3P4$$W0rD!!0194"}
    scanner_token_payload = {"expiry_minutes": 10080}

    async with AsyncClient(app=app, base_url=base_url) as ac:
        res: Response = await ac.post("/api/v1/auth/token", json=login_payload)
        res_body = res.json()
        token = res_body.get("access_token", "")

        assert res.status_code == 200
        assert token != ""
        assert token is not None

        # generate scanner token
        headers = {"Authorization": f"Bearer {token}"}

        res: Response = await ac.post(
            "/api/v1/auth/scan-token",
            json=scanner_token_payload,
            headers=headers,
        )
        res_body = res.json()

        token = res_body.get('access_token', "")
        assert res.status_code == 200
        assert token != ""
        assert token is not None
