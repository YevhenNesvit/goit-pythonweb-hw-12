from sqlalchemy.orm import Session
from app.repositories.contact_repo import ContactRepository
from app.schemas.contact import ContactCreate
from fastapi import HTTPException
from app.models.user import User


class ContactService:
    """
    Сервіс для управління контактами користувачів.

    Забезпечує CRUD операції та додаткові функції для роботи з контактами.
    """

    def __init__(self):
        self.repo = ContactRepository()

    def create_contact(self, db: Session, contact: ContactCreate, current_user: User):
        """
        Створює новий контакт для користувача.

        Args:
            db (Session): Сесія бази даних
            contact (ContactCreate): Дані нового контакту
            current_user (User): Поточний користувач

        Returns:
            Contact: Створений контакт
        """
        return self.repo.create(db, contact, current_user)

    def get_all_contacts(self, db: Session, current_user: User):
        """
        Отримує всі контакти користувача.

        Args:
            db (Session): Сесія бази даних
            current_user (User): Поточний користувач

        Returns:
            List[Contact]: Список контактів користувача
        """
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
        """
        Оновлює існуючий контакт.

        Args:
            db (Session): Сесія бази даних
            contact_id (int): ID контакту
            contact (ContactCreate): Нові дані контакту
            current_user (User): Поточний користувач

        Returns:
            Contact: Оновлений контакт

        Raises:
            HTTPException: Якщо контакт не знайдено або користувач не має прав доступу
        """
        db_contact = self.get_contact_by_id(db, contact_id, current_user)
        return self.repo.update(db, contact_id, contact)

    def delete_contact(self, db: Session, contact_id: int, current_user: User):
        """
        Видаляє контакт користувача.

        Args:
            db (Session): Сесія бази даних
            contact_id (int): ID контакту для видалення
            current_user (User): Поточний користувач

        Raises:
            HTTPException: Якщо контакт не знайдено або користувач не має прав доступу
        """
        db_contact = self.get_contact_by_id(db, contact_id, current_user)
        self.repo.delete(db, contact_id)
