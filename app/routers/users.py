from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.auth.jwt_handler import get_current_user
from app.middleware.rate_limiter import rate_limiter
import cloudinary
import cloudinary.uploader
from app.schemas.user import UserRead
import os
from dotenv import load_dotenv
from app.database import get_db, sessionmaker
from app.repositories.user_repository import UserRepository

load_dotenv()

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
async def get_current_user_info(current_user: UserRead = Depends(get_current_user), db: sessionmaker = Depends(get_db)):
    rate_limiter.check_rate_limit(str(current_user.id))
    db_user = UserRepository.get_user_by_id(db, current_user.id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)


@router.patch("/me/avatar", response_model=UserRead)
async def update_avatar(
    file: UploadFile = File(...),
    current_user: UserRead = Depends(get_current_user),
    db: sessionmaker = Depends(get_db),
):
    # Завантажуємо файл в Cloudinary
    result = cloudinary.uploader.upload(
        file.file, folder="avatars", public_id=f"user_{current_user.id}_avatar"
    )

    # Оновлюємо URL аватара користувача
    updated_user = UserRepository.update_user_avatar(db, current_user.id, result["secure_url"])
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user
