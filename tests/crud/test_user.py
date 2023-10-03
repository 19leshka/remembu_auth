import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.schemas import UserCreate
from tests.utils import random_email, random_lower_string


@pytest.mark.asyncio
async def test_create_user(db: AsyncSession):
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(password=password, email=email, full_name=email)
    user = await crud.user.add(db, obj_in=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


@pytest.mark.asyncio
async def test_authenticate_user(db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await crud.user.add(db, obj_in=user_in)
    authenticated_user = await crud.user.authenticate(
        db, email=email, password=password
    )
    assert authenticated_user
    assert user.email == authenticated_user.email
