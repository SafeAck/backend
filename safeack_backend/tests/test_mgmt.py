"""
Module for Mgmt endpoints
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
from .utils import get_user_id

# This is the same as using the @pytest.mark.anyio on all test functions in the module
pytestmark = pytest.mark.anyio


async def test_enable_user_endpoint():
    """
    Tests endpoint for enabling user
    """
    test_user_email = "testmgmtuser@example.com"
    payload = {
        "email": test_user_email,
        "first_name": "John",
        "full_name": "John Doe",
        "last_name": "Doe",
        "password": normal_user_passwd,
    }

    async with AsyncClient(app=app, base_url=base_url) as ac:
        # sign up user
        res: Response = await ac.post("/api/v1/auth/signup", json=payload)
        res_body = res.json()
        assert res.status_code == 200
        assert res_body == {"msg": "user signed up sucessfully"}

        # login with superuser
        superuser_login_payload = {
            "email": superuser_email,
            "password": superuser_passwd,
        }

        res: Response = await ac.post("/api/v1/auth/token", json=superuser_login_payload)
        res_body = res.json()
        token = res_body.get('access_token', "")

        assert res.status_code == 200
        assert token != ""
        assert token is not None

        # get user id
        user_id = get_user_id(TestingSessionLocal(), test_user_email)

        # enable user
        enable_user_payload = {"user_id": user_id}
        headers = {"Authorization": f"Bearer {token}"}
        res: Response = await ac.post(
            "/api/v1/mgmt/enable-user", json=enable_user_payload, headers=headers
        )

        res_body = res.json()
        status_code = res_body.get("status_code")
        msg = res_body.get("msg")

        assert res.status_code == 200
        assert status_code == 200
        assert msg == "User enabled successfully"


async def test_get_users():
    """
    Test get users endpoint
    """
    async with AsyncClient(app=app, base_url=base_url) as ac:
        # login as superuser
        superuser_login_payload = {
            "email": superuser_email,
            "password": superuser_passwd,
        }

        res: Response = await ac.post("/api/v1/auth/token", json=superuser_login_payload)
        res_body = res.json()
        token = res_body.get("access_token", "")

        assert res.status_code == 200
        assert token != ""
        assert token is not None

        # get users list
        superuser_logged_in_headers = {"Authorization": f"Bearer {token}"}

        user_params = {
            "page": 1,
            "limit": 3,
        }

        res: Response = await ac.get(
            "/api/v1/mgmt/users",
            params=user_params,
            headers=superuser_logged_in_headers,
        )

        users = res.json()

        assert res.status_code == 200
        assert len(users) != 0
