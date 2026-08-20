"""
Pydantic Schemas for User & Authentication
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr = Field(..., description="Valid email address")
    full_name: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Password with minimum 6 characters")
    role: Optional[str] = Field("user", description="User role ('user' or 'admin')")


class UserLogin(BaseModel):
    username_or_email: str = Field(..., description="Username or Email")
    password: str = Field(..., description="User password")


class UserResponse(UserBase):
    id: int
    is_active: bool
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int
    user: UserResponse


class TokenData(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None
