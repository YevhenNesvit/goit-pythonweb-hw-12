import redis
import json
from typing import Optional
from ..config import REDIS_HOST, REDIS_PORT


class RedisService:
    """
    Сервіс для роботи з Redis кешем.

    Забезпечує кешування даних користувачів для оптимізації продуктивності.
    """

    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

    def set_user_cache(self, user_id: int, user_data: dict, expire: int = 3600):
        """
        Зберігає дані користувача в кеші.

        Args:
            user_id (int): ID користувача
            user_data (dict): Словник з даними користувача
            expire (int): Час життя кешу в секундах (за замовчуванням 1 година)
        """
        key = f"user:{user_id}"
        self.redis_client.setex(key, expire, json.dumps(user_data))

    def get_user_cache(self, user_id: int) -> Optional[dict]:
        """
        Отримує дані користувача з кешу.

        Args:
            user_id (int): ID користувача

        Returns:
            Optional[dict]: Дані користувача або None, якщо кеш не знайдено
        """
        key = f"user:{user_id}"
        cached_user = self.redis_client.get(key)

        if cached_user:
            return json.loads(cached_user)
        return None

    def delete_user_cache(self, user_id: int):
        """
        Видаляє кеш користувача.

        Args:
            user_id (int): ID користувача
        """
        key = f"user:{user_id}"
        self.redis_client.delete(key)


redis_service = RedisService()
