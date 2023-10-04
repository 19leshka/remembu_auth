from datetime import timedelta

import bcrypt

from src.core.security import (create_access_token, get_password_hash,
                               verify_password)
from tests.utils import random_lower_string


def test_create_access_token_with_expiration():
    test_subject = random_lower_string()
    test_expires_delta = timedelta(minutes=30)
    access_token = create_access_token(test_subject, test_expires_delta)
    assert isinstance(access_token, str)


def test_create_access_token_without_expiration():
    test_subject = random_lower_string()
    access_token = create_access_token(test_subject)
    assert isinstance(access_token, str)


def test_verify_password_with_correct_password():
    plain_password = random_lower_string()
    hashed_password = get_password_hash(plain_password)
    assert verify_password(plain_password, hashed_password) is True


def test_verify_password_with_incorrect_password():
    plain_password = random_lower_string()
    hashed_password = get_password_hash(plain_password)
    assert verify_password("wrong_password", hashed_password) is False


def test_get_password_hash_generates_valid_hash():
    plain_password = random_lower_string()
    hashed_password = get_password_hash(plain_password)
    assert (
        bcrypt.checkpw(plain_password.encode("utf8"), hashed_password.encode("utf8"))
        is True
    )


def test_get_password_hash_returns_different_hashes():
    plain_password = random_lower_string()
    hashed_password1 = get_password_hash(plain_password)
    hashed_password2 = get_password_hash(plain_password)
    assert hashed_password1 != hashed_password2
