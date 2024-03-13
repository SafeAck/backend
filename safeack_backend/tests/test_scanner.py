"""
Module for testing scanner utils
"""

import pytest

from httpx import Response, AsyncClient
from . import app, base_url


# This is the same as using the @pytest.mark.anyio on all test functions in the module
pytestmark = pytest.mark.anyio


async def test_scanner_token_validation():
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

        res: Response = await ac.get("/api/v1/scanner/auth-ping", headers=headers)
        res_body = res.json()

        status_code = res_body.get("status_code", None)
        message = res_body.get("msg", None)

        assert status_code == 200
        assert message == "Authentication successful"
