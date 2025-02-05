from functools import wraps
from fastapi import HTTPException, Depends
from app.auth.jwt_handler import get_current_user
from app.models.user import UserRole

def check_role(required_role: UserRole):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user=Depends(get_current_user), **kwargs):
            if current_user.role != required_role:
                raise HTTPException(
                    status_code=403,
                    detail=f"Operation only allowed for {required_role} role"
                )
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator
