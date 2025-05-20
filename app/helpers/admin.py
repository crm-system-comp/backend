from typing import Optional, Any

from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Order


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