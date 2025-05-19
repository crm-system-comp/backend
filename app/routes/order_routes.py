from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Union
from fastapi import UploadFile, File, Form

from app.helpers.helpers import save_images
from app.database import get_db
from app.models import User, Order
from app.helpers.orders import (
    create_order, get_orders_by_user, get_order_by_id, update_order, delete_order,
)
from app.routes.dependecies import current_user
from app.schemas import OrderCreate, OrderUpdate, OrderRead, OrderType, OrderStatus

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

@order_router.put("/{order_id}", response_model=OrderUpdate)
async def update_user_order(
    order_id: int,
    order_type: OrderType = Form(...),
    status: OrderStatus = Form(...),
    size: Optional[str] = Form(None),
    style: Optional[str] = Form(None),
    quantity: Optional[int] = Form(None),
    total_price: Optional[float] = Form(None),
    full_name: Optional[str] = Form(None),
    contact_info: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_user),
):

    update_data = {
        "type": order_type,
        "status": status,
        "size": size,
        "style": style,
        "quantity": quantity,
        "total_price": total_price,
        "full_name": full_name,
        "contact_info": contact_info,
    }
    update_data = {k: v for k, v in update_data.items() if v is not None}

    updated_order = await update_order(
        db=db,
        order_id=order_id,
        user_id=user.id,
        update_data=update_data,
    )

    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")

    return updated_order

@order_router.delete("/{order_id}")
async def delete_user_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_user),
):
    order = await get_order_by_id(db, order_id)
    if not order or order.user_id != user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    success = await delete_order(db, order_id)
    return {"success": success}
