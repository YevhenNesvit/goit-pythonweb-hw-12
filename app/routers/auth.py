from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, Token
from datetime import timedelta
from app.auth.jwt_handler import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES
import secrets
from app.services.email import send_verification_email
from app.repositories.user_repository import UserRepository

router = APIRouter(tags=["Authentication"])


@router.post("/verify/{token}")
async def verify_email(token: str, db: Session = Depends(get_db)):
    user = UserRepository.verify_user_email(db, token)
    if not user:
        raise HTTPException(status_code=404, detail="Invalid verification token")

    return {"message": "Email verified successfully"}


@router.post("/register", response_model=UserRead, status_code=201)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserRepository.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    verification_token = secrets.token_urlsafe(32)
    new_user = UserRepository.create_user(db, user, verification_token)

    await send_verification_email(new_user.email, verification_token)

    return new_user


@router.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = UserRepository.get_user_by_email(db, form_data.username)
    if not user or not User.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
