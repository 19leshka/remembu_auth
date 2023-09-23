from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, models, schemas
from src.core.config import settings
from src.core.exceptions import ForbiddenException
from src.database.postgres.database import AsyncSessionFactory

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


async def get_db() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    from pydantic import ValidationError

    try:
        from src.core import security

        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise ForbiddenException
    user = crud.user.get_one(db, id_=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
