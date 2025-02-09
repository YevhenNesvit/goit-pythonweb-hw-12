from app.repositories.user_repo import UserRepository
from app.repositories.contact_repo import ContactRepository
from app.schemas.user import UserCreate
from app.models.user import UserRole


def test_create_user(db):
    repo = UserRepository()
    user_data = {
        "email": "test@example.com",
        "password": "password",
        "role": UserRole.USER,
    }
    verification_token = "test_token"

    # Створюємо об'єкт UserCreate (якщо у вас є така схема)
    # Імпортуємо схему, якщо вона є
    user_create = UserCreate(**user_data)

    # Викликаємо метод create_user з правильними аргументами
    user = repo.create_user(db, user_create, verification_token)

    # Перевіряємо результати
    assert user.email == "test@example.com"
    assert user.verification_token == verification_token
