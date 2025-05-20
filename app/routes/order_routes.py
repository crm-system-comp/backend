from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Union
from fastapi import UploadFile, File, Form

from app.helpers.helpers import save_images
from app.database import get_db
from app.models import User, Order
from app.helpers.orders import (
    create_order, get_orders_by_user, get_order_by_id,
)
from app.routes.dependecies import current_user
from app.schemas import OrderRead, OrderType

order_router = APIRouter(prefix="/api/orders")

@order_router.post("/", response_model=OrderRead)
async def create_user_order(
    order_type: OrderType = Form(...),
    size: str = Form(...),
    style: Optional[str] = Form(None),
    quantity: int = Form(...),
    total_price: float = Form(...),
    full_name: str = Form(...),
    contact_info: str = Form(...),
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_user),
):
    image_paths = await save_images(files)

    return await create_order(db, image_paths, Order(
        type=order_type,
        size=size,
        style=style,
        quantity=quantity,
        total_price=total_price,
        full_name=full_name,
        contact_info=contact_info,
        user_id=user.id
    ))

@order_router.get("/", response_model=List[OrderRead])
async def read_user_orders(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_user),
):
    return await get_orders_by_user(db, user.id)

@order_router.get("/{order_id}", response_model=OrderRead)
async def read_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_user),
):
    order = await get_order_by_id(db, order_id)
    if not order or order.user_id != user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
