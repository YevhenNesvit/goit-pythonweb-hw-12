from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from datetime import datetime, timedelta
import secrets


class UserRepository:
    """
    Репозиторій для роботи з користувачами в базі даних.
    """
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        """
        Знаходить користувача за email адресою.

        Args:
            db (Session): Сесія бази даних
            email (str): Email адреса користувача

        Returns:
            Optional[User]: Знайдений користувач або None
        """
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(db: Session, user: UserCreate, verification_token: str):
        """
        Створює нового користувача.

        Args:
            db (Session): Сесія бази даних
            user (UserCreate): Дані нового користувача
            verification_token (str): Токен для верифікації email

        Returns:
            User: Створений користувач
        """
        db_user = User(
            email=user.email,
            hashed_password=User.get_password_hash(user.password),
            role=user.role,
            verification_token=verification_token,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def verify_user_email(db: Session, token: str):
        """
        Верифікує email користувача за токеном.

        Args:
            db (Session): Сесія бази даних
            token (str): Токен верифікації

        Returns:
            Optional[User]: Користувач, який був верифікований, або None
        """
        user = db.query(User).filter(User.verification_token == token).first()
        if user:
            user.is_verified = True
            user.verification_token = None
            db.commit()
            return user
        return None

    def get_user_by_id(db: Session, user_id: int):
        """
        Отримує користувача за його ID.

        Args:
            db (Session): Сесія бази даних
            user_id (int): ID користувача

        Returns:
            Optional[User]: Знайдений користувач або None
        """
        return db.query(User).filter(User.id == user_id).first()

    def update_user_avatar(db: Session, user_id: int, avatar_url: str):
        """
        Оновлює URL аватара користувача.

        Args:
            db (Session): Сесія бази даних
            user_id (int): ID користувача
            avatar_url (str): Новий URL аватара

        Returns:
            Optional[User]: Користувач з оновленим аватаром або None
        """
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.avatar_url = avatar_url
            db.commit()
            db.refresh(user)
            return user
        return None

    def create_password_reset_token(db: Session, email: str):
        """
        Створює токен для скидання пароля.

        Args:
            db (Session): Сесія бази даних
            email (str): Email користувача

        Returns:
            Optional[str]: Токен для скидання пароля або None
        """
        user = UserRepository.get_user_by_email(db, email)
        if user:
            reset_token = secrets.token_urlsafe(32)
            user.reset_token = reset_token
            user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
            db.commit()
            return reset_token
        return None

    def reset_password(db: Session, token: str, new_password: str):
        """
        Скидає пароль користувача за токеном.

        Args:
            db (Session): Сесія бази даних
            token (str): Токен для скидання пароля
            new_password (str): Новий пароль

        Returns:
            bool: True, якщо пароль успішно скинуто, False інакше
        """
        user = (
            db.query(User)
            .filter(
                User.reset_token == token, User.reset_token_expires > datetime.utcnow()
            )
            .first()
        )

        if user:
            user.hashed_password = User.get_password_hash(new_password)
            user.reset_token = None
            user.reset_token_expires = None
            db.commit()
            return True
        return False
