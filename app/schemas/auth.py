from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

# User registration
class UserRegister(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=8)

# User login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Response token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Return user info
class UserRead(BaseModel):
    id: UUID
    email: str
    full_name: str

    class Config:
        from_attributes = True