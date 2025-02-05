import redis
import json
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

class RedisService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),  # Додайте лапки для порту
            db=0
        )

    def set_user_cache(self, user_id: int, user_data: dict, expire: int = 3600):
        """
        Кешує дані користувача в Redis
        :param user_id: ID користувача
        :param user_data: Словник з даними користувача
        :param expire: Час життя кешу в секундах (за замовчуванням 1 година)
        """
        key = f"user:{user_id}"
        self.redis_client.setex(key, expire, json.dumps(user_data))

    def get_user_cache(self, user_id: int) -> Optional[dict]:
        """
        Отримує дані користувача з кешу Redis
        :param user_id: ID користувача
        :return: Словник з даними користувача або None
        """
        key = f"user:{user_id}"
        cached_user = self.redis_client.get(key)
        
        if cached_user:
            return json.loads(cached_user)
        return None

    def delete_user_cache(self, user_id: int):
        """
        Видаляє кеш користувача
        :param user_id: ID користувача
        """
        key = f"user:{user_id}"
        self.redis_client.delete(key)

redis_service = RedisService()
