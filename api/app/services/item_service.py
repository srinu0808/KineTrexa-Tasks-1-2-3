"""
Item / Product Service Module
Business logic for CRUD, filtering, searching, and analytics.
"""
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status

from app.models.item import Item
from app.models.user import User
from app.schemas.item_schema import ItemCreate, ItemUpdate


def get_items(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    is_published: Optional[bool] = None,
    owner_id: Optional[int] = None
) -> Tuple[List[Item], int]:
    """Retrieves paginated and filtered items, returning (items, total_count)."""
    query = db.query(Item)

    if search and search.strip():
        term = f"%{search.strip()}%"
        query = query.filter((Item.title.ilike(term)) | (Item.description.ilike(term)))

    if category and category.strip():
        query = query.filter(Item.category.ilike(category.strip()))

    if min_price is not None:
        query = query.filter(Item.price >= min_price)

    if max_price is not None:
        query = query.filter(Item.price <= max_price)

    if is_published is not None:
        query = query.filter(Item.is_published == is_published)

    if owner_id is not None:
        query = query.filter(Item.owner_id == owner_id)

    total = query.count()
    items = query.order_by(Item.created_at.desc()).offset(skip).limit(limit).all()
    return items, total


def get_item_by_id(db: Session, item_id: int) -> Item:
    """Gets single item or raises 404."""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found."
        )
    return item


def create_item(db: Session, item_in: ItemCreate, current_user: User) -> Item:
    """Creates a new item owned by current_user."""
    item = Item(
        title=item_in.title,
        description=item_in.description,
        category=item_in.category,
        price=item_in.price,
        quantity=item_in.quantity,
        is_published=item_in.is_published,
        owner_id=current_user.id
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_item(db: Session, item_id: int, item_in: ItemUpdate, current_user: User) -> Item:
    """Updates an item if current user is owner or admin."""
    item = get_item_by_id(db, item_id)

    if item.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify this item."
        )

    update_data = item_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, item_id: int, current_user: User) -> Item:
    """Deletes an item if current user is owner or admin."""
    item = get_item_by_id(db, item_id)

    if item.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this item."
        )

    db.delete(item)
    db.commit()
    return item


def get_inventory_stats(db: Session) -> dict:
    """Computes overall inventory statistics."""
    total_items = db.query(Item).count()
    if total_items == 0:
        return {
            "total_items": 0,
            "total_inventory_value": 0.0,
            "categories_breakdown": {},
            "average_price": 0.0
        }

    items = db.query(Item).all()
    total_val = sum(i.price * i.quantity for i in items)
    avg_price = round(sum(i.price for i in items) / len(items), 2)

    cat_counts = {}
    for i in items:
        cat_counts[i.category] = cat_counts.get(i.category, 0) + 1

    return {
        "total_items": total_items,
        "total_inventory_value": round(total_val, 2),
        "categories_breakdown": cat_counts,
        "average_price": avg_price
    }
