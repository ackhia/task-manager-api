from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import UserRegister, Token, UserRead
from app.services.auth_service import (
    create_user,
    get_user_by_email,
    verify_password,
    create_access_token,
)
from app.api.dependencies import get_current_user  # optional for protected routes

router = APIRouter(prefix="/auth", tags=["auth"])


# --------------------------
# Register a new user
# --------------------------
@router.post("/register", response_model=UserRead)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = create_user(db, user_in.email, user_in.full_name, user_in.password)
    return user


# --------------------------
# Login user and get token
# --------------------------
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

