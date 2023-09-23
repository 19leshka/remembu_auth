from fastapi import HTTPException
from starlette import status


class DuplicatedEntryError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=message)
