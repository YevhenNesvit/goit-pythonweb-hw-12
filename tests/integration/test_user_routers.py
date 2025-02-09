import pytest
from unittest.mock import patch
from app.models.user import UserRole
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_get_current_user_info(client, token, test_user):
    with patch(
        "app.services.redis_service.RedisService.get_user_cache"
    ) as mock_get_user_cache, patch(
        "app.services.redis_service.RedisService.set_user_cache"
    ) as mock_set_user_cache:

        mock_get_user_cache.return_value = None  # Simulate a cached user
        mock_set_user_cache.return_value = None  # Avoid actual Redis operations
        # Make the request with the Authorization token
        response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == test_user.id
        assert response_data["email"] == test_user.email


@pytest.mark.asyncio
async def test_update_avatar(client, test_user, db):
    # Змінюємо роль користувача на ADMIN в базі даних
    test_user.role = UserRole.ADMIN
    db.commit()  # Після зміни ролі потрібно зробити commit в базі даних

    # Перевірка чи застосовуються зміни ролі
    assert test_user.role == UserRole.ADMIN  # Додаємо перевірку, що роль змінилась

    # Створення токену для користувача з роллю ADMIN
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.post(
            "/token",  # Шлях для отримання токену
            data={
                "username": test_user.email,
                "password": "password",
            },  # Дані для авторизації
        )
        token = response.json()["access_token"]

    # Перевірка, чи отримано правильний токен
    assert token is not None  # Перевірка, що токен не є None

    # Мокаємо операції з Redis
    with patch(
        "app.services.redis_service.RedisService.get_user_cache"
    ) as mock_get_user_cache, patch(
        "app.services.redis_service.RedisService.set_user_cache"
    ) as mock_set_user_cache:

        mock_get_user_cache.return_value = None  # Симулюємо кешованого користувача
        mock_set_user_cache.return_value = None  # Уникаємо реальних операцій з Redis

        # Підготовка файлу для завантаження
        file_data = {
            "file": ("avatar.png", open("tests/316-200x200.jpg", "rb"), "image/png")
        }

        # Виконуємо запит на оновлення аватара
        response = client.patch(
            "/users/me/avatar",  # Перевірка шляху
            files=file_data,
            headers={"Authorization": f"Bearer {token}"},
        )

        # Перевірка, чи статус код відповіді є 200 OK
        assert response.status_code == 200
        # Додаткові перевірки
        response_data = response.json()
        assert "email" in response_data  # Перевірка наявності email
        assert "id" in response_data  # Перевірка наявності id
