import os
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

DEVELOPMENT_SECRET = "development-only-change-me-before-deploying-please"
SECRET_KEY = os.getenv("HAPA_SECRET_KEY", DEVELOPMENT_SECRET)
if os.getenv("HAPA_ENVIRONMENT", "development").lower() == "production" and SECRET_KEY == DEVELOPMENT_SECRET:
    raise RuntimeError("Set HAPA_SECRET_KEY before starting Hapa Live in production")
ALGORITHM = "HS256"
COOKIE_NAME = "hapa_session"
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)


def create_session(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": str(user_id), "iat": now, "exp": now + timedelta(days=7)}, SECRET_KEY, algorithm=ALGORITHM)


def read_session(token: str) -> int | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        return None
