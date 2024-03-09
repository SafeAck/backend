"""
Module for testing root endpoints
"""

import pytest
from httpx import Response, AsyncClient
from . import app, base_url

pytestmark = pytest.mark.anyio


async def test_200_root():
    """
    Test Root View
    """
    async with AsyncClient(app=app, base_url=base_url) as ac:
        res: Response = await ac.get("/")
        assert res.status_code == 200
