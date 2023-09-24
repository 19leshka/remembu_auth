from typing import Any

from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, models, schemas
from src.api.deps import get_current_superuser, get_current_user, get_db
from src.core.exceptions import DuplicatedEntryError

router = APIRouter()


@router.post("/", response_model=schemas.User)
async def create_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(get_current_superuser),
) -> Any:
    """
    Create new user.
    """
    user = await crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise DuplicatedEntryError("A user with this email already exists")
    user = await crud.user.add(db, obj_in=user_in)
    return user


@router.post("/open", response_model=schemas.User)
async def create_user_open(
    *,
    db: AsyncSession = Depends(get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(...),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = await crud.user.get_by_email(db, email=email)
    if user:
        raise DuplicatedEntryError("A user with this email already exists")
    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
    user = await crud.user.add(db, user_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
async def read_user_me(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> schemas.User:
    """
    Get current user.
    """
    return current_user


@router.put("/me", response_model=schemas.User)
async def update_user_me(
    *,
    db: AsyncSession = Depends(get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Update ow
    """
    current_user_data = jsonable_encoder(current_user)
    user_in: schemas.UserUpdate = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = await crud.user.update(
        db,
        current_user.id,
        user_in,
    )
    return user
