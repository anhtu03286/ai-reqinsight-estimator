import uuid
import pytest
from jose import JWTError
from src.auth.jwt import create_access_token, decode_access_token, create_refresh_token, decode_refresh_token, hash_password, verify_password


def test_password_hash_verify():
    hashed = hash_password("secret123")
    assert verify_password("secret123", hashed)
    assert not verify_password("wrong", hashed)


def test_access_token_roundtrip():
    uid = str(uuid.uuid4())
    oid = str(uuid.uuid4())
    token = create_access_token(uid, oid, "ba")
    payload = decode_access_token(token)
    assert payload["sub"] == uid
    assert payload["org"] == oid
    assert payload["role"] == "ba"
    assert payload["type"] == "access"


def test_refresh_token_roundtrip():
    uid = str(uuid.uuid4())
    token = create_refresh_token(uid)
    payload = decode_refresh_token(token)
    assert payload["sub"] == uid
    assert payload["type"] == "refresh"


def test_access_token_rejected_as_refresh():
    token = create_access_token("u", "o", "admin")
    with pytest.raises(JWTError):
        decode_refresh_token(token)


def test_refresh_token_rejected_as_access():
    token = create_refresh_token("u")
    with pytest.raises(JWTError):
        decode_access_token(token)
