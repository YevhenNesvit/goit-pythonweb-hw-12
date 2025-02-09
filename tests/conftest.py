import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app.models.user import User, UserRole

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1011@localhost:5432/contacts"

test_engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest_asyncio.fixture(autouse=True)
async def clear_db():
    Base.metadata.drop_all(bind=test_engine)  # Видаляємо всі таблиці
    Base.metadata.create_all(bind=test_engine)  # Створюємо заново в SQLite
    yield
    Base.metadata.drop_all(bind=test_engine)  # Прибираємо після тестів


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    user_data = {
        "email": "test@example.com",
        "password": "password",
        "role": UserRole.USER,
    }
    user = User(
        email=user_data["email"],
        hashed_password=User.get_password_hash(user_data["password"]),
        is_verified=True,
        role=user_data["role"],
    )
    db.add(user)
    db.commit()  # Ensure async commit if using async db session
    db.refresh(user)  # Ensure async refresh
    return user


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac


@pytest_asyncio.fixture
async def token(test_user):
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.post(
            "/token", data={"username": test_user.email, "password": "password"}
        )
        return response.json()["access_token"]


@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.post(
            "/register", json={"email": "new@example.com", "password": "password"}
        )
        assert response.status_code == 201
