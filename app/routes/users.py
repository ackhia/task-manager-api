
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.services.user_service import get_user, list_users
from app.schemas.user import UserRead
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


# --------------------------
# Get current logged-in user
# --------------------------
@router.get("/me", response_model=UserRead)
def read_current_user(current_user=Depends(get_current_user)):
    """
    Returns the currently authenticated user.
    """
    return current_user


# --------------------------
# Get user by ID
# --------------------------
@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: UUID, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Get a user by their ID.
    Example: Admin-only route.
    """
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# --------------------------
# List all users
# --------------------------
@router.get("/", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    List all users.
    Example: Admin-only route. Pagination supported via skip and limit.
    """
    return list_users(db, skip=skip, limit=limit)