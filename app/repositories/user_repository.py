from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:

    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def create_user(db: Session, user: UserCreate, verification_token: str):
        db_user = User(
            email=user.email,
            hashed_password=User.get_password_hash(user.password),
            verification_token=verification_token,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def verify_user_email(db: Session, token: str):
        user = db.query(User).filter(User.verification_token == token).first()
        if user:
            user.is_verified = True
            user.verification_token = None
            db.commit()
            return user
        return None

    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def update_user_avatar(db: Session, user_id: int, avatar_url: str):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.avatar_url = avatar_url
            db.commit()
            db.refresh(user)
            return user
        return None
