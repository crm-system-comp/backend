from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import Row, RowMapping
from typing import List, Optional, Sequence, Any

from app.models import Order
from app.schemas import OrderCreate, OrderUpdate


async def create_order(
    db: AsyncSession, order_data: OrderCreate, user_id: int
) -> Order:
    new_order = Order(**order_data.dict(), user_id=user_id)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order


async def get_orders_by_user(db: AsyncSession, user_id: int) -> Sequence[Row[Any] | RowMapping | Any]:
    result = await db.execute(select(Order).where(Order.user_id == user_id))
    return result.scalars().all()


async def get_order_by_id(db: AsyncSession, order_id: int) -> Optional[Order]:
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalars().first()


async def update_order(
    db: AsyncSession, order_id: int, order_data: OrderUpdate
) -> Optional[Order]:
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    if order:
        for key, value in order_data.dict(exclude_unset=True).items():
            setattr(order, key, value)
        await db.commit()
        await db.refresh(order)
    return order


async def delete_order(db: AsyncSession, order_id: int) -> bool:
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    if order:
        await db.delete(order)
        await db.commit()
        return True
    return False
