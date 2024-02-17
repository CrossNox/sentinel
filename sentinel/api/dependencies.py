import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sentinel.config import cfg
from sentinel.config import env as current_env
from sentinel.constants import Environments
from sentinel.models.base import SessionLocal
from sentinel.utils import get_logger

logger = get_logger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_auth_header(api_key: str = Depends(APIKeyHeader(name="Authorization"))):
    if current_env != Environments.DEV:
        if not secrets.compare_digest(
            api_key.encode("utf8"), cfg.api.valid_api_key().encode("utf8")
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header does not match",
            )
