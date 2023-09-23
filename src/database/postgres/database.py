from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import as_declarative, declarative_base
from sqlalchemy.orm import declared_attr

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


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


AsyncSessionFactory = async_sessionmaker(
    class_=AsyncSession, expire_on_commit=False, bind=engine
)


async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
