"""Contains route information."""
import datetime
import time
from http.client import HTTPException

from fastapi import Request, HTTPException, status
import os
from .models import *
from arxiv.auth.user_claims import ArxivUserClaims
from arxiv.db import SessionLocal

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def is_admin_user(request: Request) -> bool:
    # temporary - use user claims in base

    user = get_current_user(request)
    if user and user.is_admin:
        return True
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def get_current_user(request: Request) -> ArxivUserClaims | None:
    session_cookie_key = request.app.extra['AUTH_SESSION_COOKIE_NAME']
    token = request.cookies.get(session_cookie_key)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    secret = request.app.extra['JWT_SECRET']
    if not secret:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    claims = ArxivUserClaims.decode_jwt_token(token, secret)
    if not claims:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return claims

def get_db():
    """Dependency for fastapi routes"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def datetime_to_epoch(timestamp: datetime.datetime | datetime.date | None,
                      default: datetime.date | datetime.datetime,
                      hour=0, minute=0, second=0) -> int:
    if timestamp is None:
        timestamp = default
    if isinstance(timestamp, datetime.date) and not isinstance(timestamp, datetime.datetime):
        # Convert datetime.date to datetime.datetime at midnight
        timestamp = datetime.datetime.combine(timestamp, datetime.time(hour, minute, second))
    # Use time.mktime() to convert datetime.datetime to epoch time
    return int(time.mktime(timestamp.timetuple()))

VERY_OLDE = datetime.datetime(1981, 1, 1)
