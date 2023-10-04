from typing import Any, Dict, Optional, Union

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import get_password_hash, verify_password
from src.crud.base import CRUDBase
from src.models.user import User
from src.schemas.user import UserCreate, UserInDB, UserUpdate


class CRUDUser(CRUDBase[User, UserInDB, UserUpdate]):
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
        model = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
        )
        session.add(model)
        await session.commit()
        await session.flush()

        try:
            await session.commit()
            return model
        except IntegrityError as e:
            await session.rollback()
            raise e

    async def update(
        self, session: AsyncSession, id_: int, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> Optional[User]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        if update_data["password"]:
            update_data["hashed_password"] = get_password_hash(update_data["password"])
            del update_data["password"]
        return await super().update(session, id_=id_, data=update_data)

    async def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
