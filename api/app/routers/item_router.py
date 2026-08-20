"""
Item & Inventory Management Router
CRUD endpoints, search, filter, pagination, and inventory statistics.
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
import math

from app.database.session import get_db
from app.models.user import User
from app.schemas.item_schema import (
    ItemCreate,
    ItemUpdate,
    ItemResponse,
    PaginatedItemsResponse,
    ItemStatsResponse
)
from app.services.auth_service import get_current_user
from app.services.item_service import (
    get_items,
    get_item_by_id,
    create_item,
    update_item,
    delete_item,
    get_inventory_stats
)

router = APIRouter(prefix="/items", tags=["Items & Inventory"])


@router.get(
    "",
    response_model=PaginatedItemsResponse,
    summary="List & Filter Items (Public / All)",
    description="Retrieves a paginated list of items with optional search and category/price filtering."
)
def list_items(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search keyword in title or description"),
    category: Optional[str] = Query(None, description="Filter by exact category"),
    min_price: Optional[float] = Query(None, ge=0.0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0.0, description="Maximum price filter"),
    is_published: Optional[bool] = Query(None, description="Filter by publication status"),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * page_size
    items, total = get_items(
        db=db,
        skip=skip,
        limit=page_size,
        search=search,
        category=category,
        min_price=min_price,
        max_price=max_price,
        is_published=is_published
    )
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    return PaginatedItemsResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=[ItemResponse.model_validate(i) for i in items]
    )


@router.get(
    "/stats/summary",
    response_model=ItemStatsResponse,
    summary="Get Inventory Statistics",
    description="Returns high-level statistics of all items including total valuation and category distribution."
)
def item_stats(db: Session = Depends(get_db)):
    return get_inventory_stats(db)


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Get Single Item by ID",
    description="Retrieves full details of an item by its unique numerical ID."
)
def get_single_item(item_id: int, db: Session = Depends(get_db)):
    item = get_item_by_id(db, item_id)
    return item


@router.post(
    "",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create New Item (Protected)",
    description="Creates a new item assigned to the authenticated user."
)
def create_new_item(
    item_in: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = create_item(db=db, item_in=item_in, current_user=current_user)
    return item


@router.put(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Update Existing Item (Protected)",
    description="Updates item properties. User must be the item owner or an admin."
)
def update_existing_item(
    item_id: int,
    item_in: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = update_item(db=db, item_id=item_id, item_in=item_in, current_user=current_user)
    return item


@router.delete(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Delete Item (Protected)",
    description="Deletes an item from the database. User must be the item owner or an admin."
)
def delete_existing_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = delete_item(db=db, item_id=item_id, current_user=current_user)
    return item
