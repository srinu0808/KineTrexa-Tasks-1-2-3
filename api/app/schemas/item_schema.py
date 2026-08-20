"""
Pydantic Schemas for Item / Product Management
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class ItemBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150, description="Title of the item")
    description: Optional[str] = Field(None, max_length=1000, description="Detailed description")
    category: str = Field("General", min_length=2, max_length=50, description="Category name")
    price: float = Field(..., ge=0.0, description="Item price (non-negative)")
    quantity: int = Field(0, ge=0, description="Available stock quantity")
    is_published: bool = Field(True, description="Publish status")


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=150)
    description: Optional[str] = Field(None, max_length=1000)
    category: Optional[str] = Field(None, min_length=2, max_length=50)
    price: Optional[float] = Field(None, ge=0.0)
    quantity: Optional[int] = Field(None, ge=0)
    is_published: Optional[bool] = None


class ItemOwner(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class ItemResponse(ItemBase):
    id: int
    owner_id: int
    owner: Optional[ItemOwner] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PaginatedItemsResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[ItemResponse]


class ItemStatsResponse(BaseModel):
    total_items: int
    total_inventory_value: float
    categories_breakdown: dict
    average_price: float
