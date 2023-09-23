from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, schemas
from src.api.deps import get_db
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
