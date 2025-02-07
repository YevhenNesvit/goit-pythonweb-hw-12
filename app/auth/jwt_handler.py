from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.services.redis_service import redis_service
from ..config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Отримує поточного користувача з JWT токена.

    Args:
        token (str): JWT токен
        db (Session): Сесія бази даних

    Returns:
        User: Поточний користувач

    Raises:
        HTTPException: Якщо токен недійсний або користувач не знайдений
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Спочатку перевіряємо Redis кеш
    cached_user = redis_service.get_user_cache(payload.get("user_id"))
    if cached_user:
        return User(**cached_user)

    # Якщо в кеші немає, шукаємо в базі даних
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    # Кешуємо користувача
    redis_service.set_user_cache(
        user.id,
        {
            "id": user.id,
            "email": user.email,
            "is_verified": user.is_verified,
            "avatar_url": user.avatar_url,
        },
    )

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Створює JWT токен доступу.

    Args:
        data (dict): Дані для включення в токен
        expires_delta (Optional[timedelta]): Термін дії токена

    Returns:
        str: Згенерований JWT токен
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
