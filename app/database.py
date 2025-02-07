from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DATABASE_URL

# Підключення до PostgreSQL
engine = create_engine(DATABASE_URL)

# Створення сесій
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовий клас для моделей
Base = declarative_base()


# Функція для отримання сесії
def get_db():
    """
    Генерує сесію бази даних для використання в залежностях FastAPI.

    Yields:
        Session: Сесія бази даних

    Приклад використання:
        db = next(get_db())
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
