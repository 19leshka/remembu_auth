from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.core.config import settings

url = (
    f"postgresql+asyncpg://"
    f"{settings.PG_USER}:"
    f"{settings.PG_PASS}@"
    f"{settings.PG_HOST}:"
    f"{settings.PG_PORT}/"
    f"{settings.PG_DB}"
)


engine = create_async_engine(url, echo=True)
Base = declarative_base()


AsyncSessionFactory = async_sessionmaker(
    class_=AsyncSession, expire_on_commit=False, bind=engine
)


async def get_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session


async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
