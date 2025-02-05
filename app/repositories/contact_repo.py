from sqlalchemy.orm import Session
from app.models.contact import Contact
from app.schemas.contact import ContactCreate
from app.models.user import User


class ContactRepository:
    def create(self, db: Session, contact: ContactCreate, user: User):
        contact_data = contact.model_dump()
        new_contact = Contact(**contact_data, user_id=user.id)
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        return new_contact

    def get_user_contacts(self, db: Session, user: User):
        return db.query(Contact).filter(Contact.user_id == user.id).all()

    def get_by_id(self, db: Session, contact_id: int):
        return db.query(Contact).filter(Contact.id == contact_id).first()

    def update(self, db: Session, contact_id: int, contact: ContactCreate):
        db_contact = self.get_by_id(db, contact_id)
        if db_contact:
            for key, value in contact.model_dump().items():
                setattr(db_contact, key, value)
            db.commit()
            db.refresh(db_contact)
        return db_contact

    def delete(self, db: Session, contact_id: int):
        db_contact = self.get_by_id(db, contact_id)
        if db_contact:
            db.delete(db_contact)
            db.commit()
