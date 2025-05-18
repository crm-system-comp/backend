from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.models import User
from app.auth.auth import auth_backend
from app.auth.manager import get_user_manager
from app.helpers.orders import (
    create_order, get_orders_by_user, get_order_by_id, update_order, delete_order,
)
from app.routes.dependecies import current_user
from app.schemas import OrderCreate, OrderUpdate, OrderRead


order_router = APIRouter()

@order_router.post("/", response_model=OrderRead)
async def create_user_order(
    order: OrderCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_user),
):
    return await create_order(db, order, user.id)


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


@order_router.put("/{order_id}", response_model=OrderRead)
async def update_user_order(
    order_id: int,
    order_data: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_user),
):
    order = await get_order_by_id(db, order_id)
    if not order or order.user_id != user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    return await update_order(db, order_id, order_data)


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
