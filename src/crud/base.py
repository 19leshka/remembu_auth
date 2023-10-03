from typing import Generic, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import Result, and_, delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import expression

from src.database.postgres.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def filter_query(self, query: expression, kwargs: dict) -> expression:
        filter_list = [
            getattr(self.model, key) == value for key, value in kwargs.items()
        ]
        return query.where(and_(True, *filter_list))

    async def get_one(self, session: AsyncSession, id_: int) -> Optional[ModelType]:
        query = select(self.model).filter(self.model.id == id_)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_list(
        self, session: AsyncSession, *, skip: int = 0, limit: int = 100, **kwargs
    ) -> [ModelType]:
        query = self.filter_query(query=select(self.model), kwargs=kwargs)
        result: Result = await session.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    async def add(
        self, session: AsyncSession, obj_in: CreateSchemaType
    ) -> Optional[ModelType]:
        model = self.model(**(obj_in if isinstance(obj_in, dict) else dict(obj_in)))
        session.add(model)
        await session.flush()
        try:
            await session.commit()
            return model
        except IntegrityError as e:
            await session.rollback()
            raise e

    async def update(
        self, session: AsyncSession, id_: int, data: UpdateSchemaType
    ) -> Optional[ModelType]:
        query = (
            update(self.model)
            .where(self.model.id == id_)
            .values(**(dict(data)))
            .returning(self.model)
        )
        new = await session.execute(query)
        await session.flush()
        try:
            await session.commit()
            return new.fetchone()
        except IntegrityError as e:
            await session.rollback()
            raise e

    def delete(self, session: AsyncSession, *, id_: int) -> None:
        session.execute(delete(self.model).filter(self.model.id == id_))
        session.commit()
