from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.auth.jwt_handler import get_current_user
from app.middleware.rate_limiter import rate_limiter
import cloudinary
import cloudinary.uploader
from app.schemas.user import UserRead, UserCreate
from app.database import get_db, sessionmaker
from app.repositories.user_repo import UserRepository
from app.auth.permissions import check_role
from app.models.user import UserRole, User
from sqlalchemy.orm import Session
from ..config import CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, CLOUDINARY_CLOUD_NAME
import secrets

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
async def get_current_user_info(
    current_user: UserRead = Depends(get_current_user),
    db: sessionmaker = Depends(get_db),
):
    """
    Отримує інформацію про поточного користувача.

    Args:
        current_user (UserRead): Поточний користувач
        db (sessionmaker): Сесія бази даних

    Returns:
        UserRead: Інформація про користувача

    Raises:
        HTTPException: Якщо користувача не знайдено
    """
    rate_limiter.check_rate_limit(str(current_user.id))
    db_user = UserRepository.get_user_by_id(db, current_user.id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
)


@router.patch("/me/avatar", response_model=UserRead)
@check_role(UserRole.ADMIN)
async def update_avatar(
    file: UploadFile = File(...),
    current_user: UserRead = Depends(get_current_user),
    db: sessionmaker = Depends(get_db),
):
    """
    Оновлює аватар користувача.

    Args:
        file (UploadFile): Файл зображення для аватара
        current_user (UserRead): Поточний користувач
        db (sessionmaker): Сесія бази даних

    Returns:
        UserRead: Користувач з оновленим аватаром

    Raises:
        HTTPException: Якщо користувача не знайдено
    """
    result = cloudinary.uploader.upload(
        file.file, folder="avatars", public_id=f"user_{current_user.id}_avatar"
    )

    updated_user = UserRepository.update_user_avatar(
        db, current_user.id, result["secure_url"]
    )
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user


@router.post("/admin", response_model=UserRead)
@check_role(UserRole.ADMIN)
async def create_admin(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Створює нового адміністратора.

    Args:
        user (UserCreate): Дані нового адміністратора
        db (Session): Сесія бази даних
        current_user (User): Поточний користувач

    Returns:
        UserRead: Створений адміністратор
    """

    verification_token = secrets.token_urlsafe(32)
    user.role = UserRole.ADMIN
    db_user = UserRepository.create_user(db, user, verification_token)
    return db_user
