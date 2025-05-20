from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database import get_db
from app.helpers.admin import update_order_admin, delete_order_admin
from app.helpers.helpers import is_admin
from app.models import User, Order
from app.schemas import UserOut, OrderRead, OrderStatus, OrderType
from app.routes.dependecies import current_user

from sqlalchemy.future import select

admin_router = APIRouter(prefix="/api/admin")

@admin_router.get("/users", response_model=List[UserOut])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_user),
):
    is_admin(user)
    result = await db.execute(select(User))
    return result.scalars().all()


@admin_router.get("/orders", response_model=List[OrderRead])
async def get_all_orders(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_user),
):
    is_admin(user)
    result = await db.execute(select(Order))
    return result.scalars().all()


@admin_router.put("/orders/{order_id}", response_model=OrderRead)
async def admin_update_order(
    order_id: int,
    order_type: OrderType,
    status: OrderStatus,
    size: Optional[str] = None,
    style: Optional[str] = None,
    quantity: Optional[int] = None,
    total_price: Optional[float] = None,
    full_name: Optional[str] = None,
    contact_info: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_user),
):
    is_admin(user)

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

    updated_order = await update_order_admin(db, order_id, update_data)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
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
        raise HTTPException(status_code=404, detail="Order not found")
    return {"success": True}
