import asyncio

import pytest
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from src.core.config import settings
from src.database.postgres.database import Base

engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
)

async_session_maker = async_sessionmaker(
    class_=AsyncSession, expire_on_commit=False, bind=engine
)


@pytest.fixture(scope="session", autouse=True)
async def init_db():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def db():
    async with async_session_maker() as session:
        yield session
        await session.rollback()
        await session.close()


@pytest.fixture(scope="function", autouse=True)
async def auto_rollback(db: AsyncSession):
    await db.rollback()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
