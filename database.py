from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import settings
from models.models import Base, TasksOrm, UsersOrm


metadata_obj = Base.metadata


engine = create_async_engine(
    url=settings.async_pg_db,
    echo=True
)


session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False
    )


# async def get_session():
#     async with session_factory() as session:
#         yield session


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(metadata_obj.create_all)