"""
SQLAlchemy Item / Product Model
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.session import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), index=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), index=True, nullable=False, default="General")
    price = Column(Float, nullable=False, default=0.0)
    quantity = Column(Integer, nullable=False, default=0)
    is_published = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="items")
