from enum import Enum
from typing import Optional
from pydantic import BaseModel
from fastapi_users import schemas

class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True

class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: Optional[str] = None
    photo: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

class BaseUser(BaseModel):
    username: str
    email: str
    photo: str

class UserOut(BaseUser):
    id: int

    class Config:
        orm_mode = True

class OrderStatus(str, Enum):
    QUEUED = "в очереди"
    PROCESSING = "обработка"
    PRINTING = "печать"
    SHIPPING = "отправка товара"
    COMPLETED = "завершено"


class OrderType(str, Enum):
    PAINTING = "картина"
    POSTER = "постер"


class OrderBase(BaseModel):
    type: OrderType
    size: str
    style: Optional[str]
    quantity: int
    image_path: Optional[str]
    total_price: float
    full_name: str
    contact_info: str
    status: Optional[OrderStatus] = OrderStatus.QUEUED


class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    size: Optional[str]
    style: Optional[str]
    quantity: Optional[int]
    image_path: Optional[str]
    total_price: Optional[float]
    status: Optional[OrderStatus]


class OrderRead(OrderBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True