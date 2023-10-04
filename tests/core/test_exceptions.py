from fastapi import HTTPException
from starlette import status

from src.core.exceptions import (DuplicatedEntryError, ForbiddenException,
                                 NotFoundException)


def test_duplicated_entry_error():
    message = "Duplicate entry found."
    try:
        raise DuplicatedEntryError(message)
    except HTTPException as exc:
        assert exc.status_code == status.HTTP_409_CONFLICT
        assert exc.detail == message


def test_forbidden_exception():
    message = "Access forbidden."
    try:
        raise ForbiddenException(message)
    except HTTPException as exc:
        assert exc.status_code == status.HTTP_403_FORBIDDEN
        assert exc.detail == message


def test_not_found_exception():
    message = "Resource not found."
    try:
        raise NotFoundException(message)
    except HTTPException as exc:
        assert exc.status_code == status.HTTP_404_NOT_FOUND
        assert exc.detail == message
