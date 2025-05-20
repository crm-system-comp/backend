from typing import List

from dotenv import load_dotenv
from sqlalchemy import select

from app.consts import STATIC_PATH, BASE_URL
from app.database import Base, engine, async_session
import os
from uuid import uuid4
from fastapi import UploadFile, HTTPException
from passlib.context import CryptContext

from app.models import User
load_dotenv()

async def to_start():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def create_admin():
    async with async_session() as session:
        result = await session.execute(select(User).where(User.is_superuser == True))
        admin = result.scalars().first()
        if not admin:
            admin = User(
                email="admin@example.com",
                username="admin",
                hashed_password=get_password_hash(os.getenv("ADMIN_PASSWORD")),
                is_superuser=True,
                is_active=True,
                is_verified=True,
            )
            session.add(admin)
            await session.commit()

async def to_shutdown():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def save_images(files: List[UploadFile]) -> List[str]:
    image_paths = []
    os.makedirs(STATIC_PATH, exist_ok=True)

    for file in files:
        ext = file.filename.split(".")[-1]
        unique_name = f"{uuid4()}.{ext}"
        full_path = os.path.join(STATIC_PATH, unique_name)

        with open(full_path, "wb") as f:
            content = await file.read()
            f.write(content)

        public_url = f"{BASE_URL}/static/{unique_name}"
        image_paths.append(public_url)

    return image_paths

def is_admin(user: User):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized as admin")
    return user
