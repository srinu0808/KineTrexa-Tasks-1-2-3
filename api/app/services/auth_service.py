"""
Authentication Service & Current User Dependency
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.database.session import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin, TokenResponse, UserResponse
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    security_bearer
)
from app.core.config import settings


def register_new_user(db: Session, user_in: UserCreate) -> User:
    """Registers a new unique user."""
    existing_username = db.query(User).filter(User.username == user_in.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username '{user_in.username}' is already registered."
        )

    existing_email = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{user_in.email}' is already registered."
        )

    hashed_pw = hash_password(user_in.password)
    user = User(
        username=user_in.username,
        email=user_in.email.lower(),
        full_name=user_in.full_name,
        hashed_password=hashed_pw,
        role=user_in.role or "user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, credentials: UserLogin) -> TokenResponse:
    """Authenticates credentials and returns JWT Bearer token."""
    login_ident = credentials.username_or_email.strip()
    user = db.query(User).filter(
        (User.username == login_ident) | (User.email == login_ident.lower())
    ).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive."
        )

    token_payload = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role
    }
    access_token = create_access_token(data=token_payload)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        user=UserResponse.model_validate(user)
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_bearer),
    db: Session = Depends(get_db)
) -> User:
    """Dependency for securing endpoints requiring an authenticated User."""
    token = credentials.credentials
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload."
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Authenticated user no longer exists."
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated."
        )
    return user
