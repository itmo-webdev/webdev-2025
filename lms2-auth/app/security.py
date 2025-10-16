from datetime import datetime, timedelta
from jose import jwt
from argon2 import PasswordHasher
from uuid import uuid4
from .config import settings

ph = PasswordHasher()

def hash_password(pw: str) -> str:
    return ph.hash(pw)

def verify_password(pw: str, pw_hash: str) -> bool:
    try:
        ph.verify(pw_hash, pw)
        return True
    except Exception:
        return False

def make_access_token(sub: str):
    payload = {"sub": sub, "type":"access"}
    return jwt.encode(payload | {"exp": datetime.utcnow()+timedelta(minutes=settings.ACCESS_EXPIRES_MIN)},
                      settings.JWT_SECRET, algorithm=settings.JWT_ALG)

def make_refresh_token(sub: str, jti: str):
    payload = {"sub": sub, "jti": jti, "type":"refresh"}
    return jwt.encode(payload | {"exp": datetime.utcnow()+timedelta(days=settings.REFRESH_EXPIRES_DAYS)},
                      settings.JWT_SECRET, algorithm=settings.JWT_ALG)

def decode_token(token: str):
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
