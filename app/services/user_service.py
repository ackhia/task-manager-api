
from uuid import UUID

from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate

# ----------------------------
# Get a single user by ID
# ----------------------------
def get_user(db: Session, user_id: UUID) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


# ----------------------------
# Get a single user by email
# ----------------------------
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


# ----------------------------
# List all users (optional pagination can be added later)
# ----------------------------
def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


# ----------------------------
# Create a new user
# ----------------------------
def create_user(db: Session, user_in: UserCreate) -> User:
    from app.services.auth_service import hash_password  # import here to avoid circular imports
    
    hashed_password = hash_password(user_in.password)
    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ----------------------------
# Update an existing user
# ----------------------------
def update_user(db: Session, user: User, full_name: Optional[str] = None, is_active: Optional[bool] = None) -> User:
    if full_name is not None:
        user.full_name = full_name
    if is_active is not None:
        user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user