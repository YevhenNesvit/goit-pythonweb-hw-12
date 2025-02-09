from app.repositories.contact_repo import ContactRepository
from app.schemas.contact import ContactCreate
import pytest
from unittest.mock import MagicMock
from app.models.user import User
from app.models.contact import Contact

@pytest.mark.asyncio
async def test_create_contact_repo(db, test_user):
    actual_user = test_user
    repo = ContactRepository()
    contact_data = ContactCreate(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="1234567890",
        birthday="1990-01-01"
    )
    contact = repo.create(db, contact_data, actual_user)
