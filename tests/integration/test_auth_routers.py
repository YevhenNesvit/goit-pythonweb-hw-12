import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/register", json={"email": "new@example.com", "password": "password"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "new@example.com"
