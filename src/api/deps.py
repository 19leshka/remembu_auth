from sqlalchemy.ext.asyncio import AsyncSession

from src.database.postgres.database import AsyncSessionFactory


async def get_db() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session
