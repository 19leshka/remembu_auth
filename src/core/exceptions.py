from fastapi import HTTPException
from starlette import status


class DuplicatedEntryError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=message)


class ForbiddenException(HTTPException):
    def __init__(self, message):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=message)
