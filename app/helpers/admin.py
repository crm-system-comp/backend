from typing import Optional, Any

from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Order, User

async def select_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    user_data = result.scalar_one_or_none()
    return user_data

async def select_all_orders(db: AsyncSession):
    result = await db.execute(select(Order))
    return result.scalars().all()

async def select_all_users(db: AsyncSession):
    result = await db.execute(select(User).where(User.is_superuser is not True))
    return result.scalars().all()

async def update_order_admin(
    db: AsyncSession,
    order_id: int,
    update_data: dict,
) -> None | Row[Any] | RowMapping:
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()

    if not order:
        return None

    for key, value in update_data.items():
        setattr(order, key, value)

    await db.commit()
    await db.refresh(order)
    return order


async def delete_order_admin(db: AsyncSession, order_id: int) -> bool:
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    if order:
        for image in order.images:
            await db.delete(image)
        await db.delete(order)
        await db.commit()
        return True
    return False