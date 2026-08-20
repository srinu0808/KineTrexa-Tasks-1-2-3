"""
SQLAlchemy User Model
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default="user")  # 'admin' or 'user'
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    items = relationship("Item", back_populates="owner", cascade="all, delete-orphan")
