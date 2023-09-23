from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import get_password_hash, verify_password
from src.crud.base import CRUDBase
from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(
        self, session: AsyncSession, *, email: str
    ) -> Optional[User]:
        query = select(self.model).filter(self.model.email == email)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def authenticate(
        self, session: AsyncSession, *, email: str, password: str
    ) -> Optional[User]:
        user: User = await self.get_by_email(session, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def add(self, session: AsyncSession, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
        )
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
