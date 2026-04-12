from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models import User

# ----------------------------
# JWT Settings (use env variables in prod!)
# ----------------------------
SECRET_KEY = "YOUR_SECRET_KEY"  # Replace with an environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ----------------------------
# Password Hashing
# ----------------------------
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


# ----------------------------
# JWT Token
# ----------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


# ----------------------------
# Database Operations
# ----------------------------
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Find a user by email."""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email: str, full_name: str, password: str) -> User:
    """Create a new user with hashed password."""
    hashed_password = hash_password(password)
    user = User(email=email, full_name=full_name, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user