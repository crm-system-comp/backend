from typing import List

from app.consts import STATIC_PATH, BASE_URL
from app.database import Base, engine
import os
from uuid import uuid4
from fastapi import UploadFile

async def to_start():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

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
