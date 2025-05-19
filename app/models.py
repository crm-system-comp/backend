from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Float
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from app.database import Base, get_db
from app.schemas import OrderType, OrderStatus

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    orders = relationship("Order", back_populates="user")

async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    type = Column(Enum(OrderType), nullable=False)
    size = Column(String, nullable=False)
    style = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    image_path = Column(String, nullable=True)
    total_price = Column(Float, nullable=False)

    full_name = Column(String, nullable=False)
    contact_info = Column(String, nullable=False)

    status = Column(Enum(OrderStatus), default=OrderStatus.QUEUED, nullable=False)

    user = relationship("User", back_populates="orders")
    images = relationship("Image", back_populates="order", cascade="all, delete-orphan", lazy="selectin")

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    path = Column(String, nullable=False)

    order_id = Column(Integer, ForeignKey("orders.id"))
    order = relationship("Order", back_populates="images", lazy="selectin")