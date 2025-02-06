from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from passlib.context import CryptContext
import enum

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER)

    contacts = relationship("Contact", back_populates="user")

    def get_password_hash(password: str):
        """
        Створює хеш пароля.

        Args:
            password (str): Пароль у відкритому вигляді

        Returns:
            str: Хешований пароль
        """
        return pwd_context.hash(password)

    def verify_password(plain_password: str, hashed_password: str):
        """
        Перевіряє відповідність пароля його хешу.

        Args:
            plain_password (str): Пароль у відкритому вигляді
            hashed_password (str): Хешований пароль

        Returns:
            bool: True якщо пароль відповідає хешу, False інакше
        """
        return pwd_context.verify(plain_password, hashed_password)
