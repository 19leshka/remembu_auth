from typing import Any

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, declared_attr

from src.core.config import settings

url = (
    f"postgresql+asyncpg://"
    f"{settings.PG_USER}:"
    f"{settings.PG_PASS}@"
    f"{settings.PG_HOST}:"
    f"{settings.PG_PORT}/"
    f"{settings.PG_DB}"
)


POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)

engine = create_async_engine(url, echo=True)


class Base(DeclarativeBase):
    id: Any
    __name__: str
    metadata = metadata

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
