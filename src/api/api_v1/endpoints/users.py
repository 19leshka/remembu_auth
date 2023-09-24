from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, models, schemas
from src.api.deps import get_current_user, get_db
from src.core.exceptions import DuplicatedEntryError

router = APIRouter()


@router.post("/", response_model=schemas.User)
async def create_user(
    *, db: AsyncSession = Depends(get_db), user_in: schemas.UserCreate
) -> Any:
    """
    Create new user.
    """
    user = await crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise DuplicatedEntryError("A user with this email already exists")
    user = await crud.user.add(db, obj_in=user_in)
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
