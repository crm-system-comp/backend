from app.database import Base, engine

async def to_start():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def to_shutdown():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)