import pytest
from app.main import app
from unittest.mock import patch


@pytest.mark.asyncio
async def test_create_contact(async_client, token):
    with patch(
        "app.services.redis_service.RedisService.get_user_cache"
    ) as mock_get_user_cache, patch(
        "app.services.redis_service.RedisService.set_user_cache"
    ) as mock_set_user_cache:

        mock_get_user_cache.return_value = None  # Simulate a cached user
        mock_set_user_cache.return_value = None  # Avoid actual Redis operations

        token_value = token
        response = await async_client.post(
            "/contacts/",
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "1234567890",
                "birthday": "1990-01-01",
            },
            headers={"Authorization": f"Bearer {token_value}"},
        )

        assert response.status_code == 201
