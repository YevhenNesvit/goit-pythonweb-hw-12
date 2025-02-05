from fastapi import APIRouter, Depends, UploadFile, File
from app.auth.jwt_handler import get_current_user
from app.middleware.rate_limiter import rate_limiter
import cloudinary
import cloudinary.uploader
from app.schemas.user import UserRead
import os
from dotenv import load_dotenv
from app.database import get_db, sessionmaker

load_dotenv()

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
async def get_current_user_info(current_user: UserRead = Depends(get_current_user)):
    rate_limiter.check_rate_limit(str(current_user.id))
    return current_user


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)


# Додамо ендпоінт для оновлення аватара
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
    current_user.avatar_url = result["secure_url"]
    db.commit()

    return current_user
