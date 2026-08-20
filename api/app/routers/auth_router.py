"""
Authentication & User Router
Endpoints for Registration, Login (JWT), and User Profile.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse, TokenResponse
from app.models.user import User
from app.services.auth_service import register_new_user, authenticate_user, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register New User",
    description="Registers a new user account with unique username and email."
)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = register_new_user(db, user_in)
    return user


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="User Login (JWT Authentication)",
    description="Authenticates user credentials and returns a secure JWT access token."
)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    token_response = authenticate_user(db, credentials)
    return token_response


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Current User Profile",
    description="Retrieves the profile of the currently authenticated user using JWT Bearer token."
)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user
