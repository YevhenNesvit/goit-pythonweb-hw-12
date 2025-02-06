from fastapi import HTTPException
import time
from collections import defaultdict
from typing import Dict, List


class RateLimiter:
    """
    Middleware для обмеження кількості запитів.

    Attributes:
        requests_per_minute (int): Максимальна кількість запитів за хвилину
        requests (Dict[str, List[float]]): Словник для відстеження запитів
    """

    def __init__(self, requests_per_minute: int = 10):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, List[float]] = defaultdict(list)

    def check_rate_limit(self, user_id: str):
        """
        Перевіряє, чи не перевищено ліміт запитів для користувача.

        Args:
            user_id (str): Ідентифікатор користувача

        Raises:
            HTTPException: Якщо перевищено ліміт запитів
        """
        now = time.time()
        minute_ago = now - 60

        # Видаляємо старі запити
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id] if req_time > minute_ago
        ]

        # Перевіряємо ліміт
        if len(self.requests[user_id]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429, detail="Too many requests. Please try again later."
            )

        # Додаємо новий запит
        self.requests[user_id].append(now)


rate_limiter = RateLimiter()
