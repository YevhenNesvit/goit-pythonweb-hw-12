from sqlalchemy.orm import Session
from app.repositories.contact_repo import ContactRepository
from app.schemas.contact import ContactCreate
from fastapi import HTTPException
from app.models.user import User


class ContactService:
    def __init__(self):
        self.repo = ContactRepository()

    def create_contact(self, db: Session, contact: ContactCreate, current_user: User):
        return self.repo.create(db, contact, current_user)

    def get_all_contacts(self, db: Session, current_user: User):
        return self.repo.get_user_contacts(db, current_user)

    def get_contact_by_id(self, db: Session, contact_id: int, current_user: User):
        contact = self.repo.get_by_id(db, contact_id)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        if contact.user_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="Not authorized to access this contact"
            )
        return contact

    def update_contact(
        self, db: Session, contact_id: int, contact: ContactCreate, current_user: User
    ):
        db_contact = self.get_contact_by_id(db, contact_id, current_user)
        return self.repo.update(db, contact_id, contact)

    def delete_contact(self, db: Session, contact_id: int, current_user: User):
        db_contact = self.get_contact_by_id(db, contact_id, current_user)
        self.repo.delete(db, contact_id)
