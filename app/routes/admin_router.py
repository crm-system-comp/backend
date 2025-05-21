from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database import get_db
from app.helpers.admin import update_order_admin, delete_order_admin, select_all_users, select_user_by_id, \
    select_all_orders
from app.helpers.helpers import is_admin
from app.models import User, Order
from app.schemas import UserOut, OrderRead, OrderStatus, OrderType, OrderUpdate
from app.routes.dependecies import current_user

from sqlalchemy.future import select

admin_router = APIRouter(prefix="/api/admin")

@admin_router.get("/users", response_model=List[UserOut])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_user),
):
    is_admin(user)
    return await select_all_users(db)

@admin_router.get("/users/{user_id}", response_model=UserOut)
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_user),
):
    is_admin(user)
    user_data = await select_user_by_id(db, user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user_data

@admin_router.get("/orders", response_model=List[OrderRead])
async def get_all_orders(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_user),
):
    is_admin(user)
    return await select_all_orders(db)

@admin_router.put("/orders/{order_id}", response_model=OrderRead)
async def admin_update_order(
    order_id: int,
    update_data: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_user),
):
    is_admin(user)
    update_dict = update_data.dict(exclude_unset=True)

    updated_order = await update_order_admin(db, order_id, update_dict)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return updated_order

@admin_router.delete("/orders/{order_id}")
async def admin_delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_user),
):
    is_admin(user)
    success = await delete_order_admin(db, order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return {"success": True}
