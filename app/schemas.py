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