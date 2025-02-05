from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.contact import ContactCreate, ContactRead
from app.services.contact_service import ContactService
from app.database import get_db
from app.models.contact import Contact
from typing import List, Optional
from app.auth.jwt_handler import get_current_user
from app.models.user import User

router = APIRouter(prefix="/contacts", tags=["Contacts"])
service = ContactService()


@router.get("/search", response_model=List[ContactRead])
def search_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
):
    query = db.query(Contact).filter(Contact.user_id == current_user.id)

    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))

    contacts = query.all()
    return contacts


@router.post("/", response_model=ContactRead, status_code=201)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.create_contact(db, contact, current_user)


@router.get("/", response_model=List[ContactRead])
def list_contacts(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return service.get_all_contacts(db, current_user)


@router.get("/{contact_id}", response_model=ContactRead)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_contact_by_id(db, contact_id, current_user)


@router.put("/{contact_id}", response_model=ContactRead)
def update_contact(
    contact_id: int,
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.update_contact(db, contact_id, contact, current_user)


@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service.delete_contact(db, contact_id, current_user)
    return {"detail": "Contact deleted"}


@router.get("/birthdays/next7", response_model=List[ContactRead])
def get_contacts_with_birthdays_next_7_days(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    today = datetime.today()
    next_week = today + timedelta(days=7)

    contacts = (
        db.query(Contact)
        .filter(
            (Contact.birthday >= today)
            & (Contact.birthday <= next_week)
            & (Contact.user_id == current_user.id)
        )
        .all()
    )

    return contacts
