from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import Row, RowMapping
from typing import List, Optional, Sequence, Any

from app.helpers.helpers import save_images
from app.models import Order, Image
from app.schemas import OrderUpdate, OrderRead, OrderBase


async def create_order(
    db: AsyncSession, images: List[str], order_data: OrderRead
) -> OrderBase:
    for path in images:
        order_data.images.append(Image(path=path))

    db.add(order_data)
    await db.commit()
    await db.refresh(order_data)
    return order_data

async def get_orders_by_user(db: AsyncSession, user_id: int) -> Sequence[Order]:
    result = await db.execute(select(Order).where(Order.user_id == user_id))
    return result.scalars().all()


async def get_order_by_id(db: AsyncSession, order_id: int) -> Optional[Order]:
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalars().first()

async def update_order(
    db: AsyncSession,
    order_id: int,
    user_id: int,
    update_data: dict,
) -> Optional[Order]:
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()

    if not order or order.user_id != user_id:
        return None

    for key, value in update_data.items():
        setattr(order, key, value)

    await db.commit()
    await db.refresh(order)
    return order


async def delete_order(db: AsyncSession, order_id: int) -> bool:
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    if order:
        for image in order.images:
            await db.delete(image)
        await db.delete(order)
        await db.commit()
        return True
    return False
