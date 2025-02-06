from sqlalchemy.orm import Session
from app.models.contact import Contact
from app.schemas.contact import ContactCreate
from app.models.user import User


class ContactRepository:
    """
    Репозиторій для роботи з контактами в базі даних.
    """

    def create(self, db: Session, contact: ContactCreate, user: User):
        """
        Створює новий контакт для користувача.

        Args:
            db (Session): Сесія бази даних
            contact (ContactCreate): Дані нового контакту
            user (User): Користувач, якому належить контакт

        Returns:
            Contact: Створений контакт
        """
        contact_data = contact.model_dump()
        new_contact = Contact(**contact_data, user_id=user.id)
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        return new_contact

    def get_user_contacts(self, db: Session, user: User):
        """
        Отримує всі контакти користувача.

        Args:
            db (Session): Сесія бази даних
            user (User): Користувач, контакти якого потрібно отримати

        Returns:
            List[Contact]: Список контактів користувача
        """
        return db.query(Contact).filter(Contact.user_id == user.id).all()

    def get_by_id(self, db: Session, contact_id: int):
        """
        Отримує контакт за його ID.

        Args:
            db (Session): Сесія бази даних
            contact_id (int): ID контакту

        Returns:
            Optional[Contact]: Знайдений контакт або None
        """
        return db.query(Contact).filter(Contact.id == contact_id).first()

    def update(self, db: Session, contact_id: int, contact: ContactCreate):
        """
        Оновлює існуючий контакт.

        Args:
            db (Session): Сесія бази даних
            contact_id (int): ID контакту
            contact (ContactCreate): Нові дані контакту

        Returns:
            Optional[Contact]: Оновлений контакт або None, якщо контакт не знайдено
        """
        db_contact = self.get_by_id(db, contact_id)
        if db_contact:
            for key, value in contact.model_dump().items():
                setattr(db_contact, key, value)
            db.commit()
            db.refresh(db_contact)
        return db_contact

    def delete(self, db: Session, contact_id: int):
        """
        Видаляє контакт за його ID.

        Args:
            db (Session): Сесія бази даних
            contact_id (int): ID контакту для видалення

        Returns:
            None
        """
        db_contact = self.get_by_id(db, contact_id)
        if db_contact:
            db.delete(db_contact)
            db.commit()
