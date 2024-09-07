"""Contains route information."""
import datetime
import time
from http.client import HTTPException
from logging import getLogger

from fastapi import Request, HTTPException, status
import os

import jwt
import jwcrypto
import jwcrypto.jwt

from .models import *
from arxiv.auth.user_claims import ArxivUserClaims
from arxiv.auth.openid.oidc_idp import ArxivOidcIdpClient
from arxiv.db import SessionLocal

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

class AccessTokenExpired(Exception):
    pass


async def is_admin_user(request: Request) -> bool:
    # temporary - use user claims in base

    user = await get_current_user(request)
    if user and user.is_admin:
        return True
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


async def is_any_user(request: Request) -> bool:
    user = await get_current_user(request)
    if user:
        return True
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


async def get_current_user(request: Request) -> ArxivUserClaims | None:
    logger = getLogger(__name__)
    session_cookie_key = request.app.extra['AUTH_SESSION_COOKIE_NAME']
    token = request.cookies.get(session_cookie_key)
    if not token:
        logger.debug(f"There is no cookie '{session_cookie_key}'")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    secret = request.app.extra['JWT_SECRET']
    if not secret:
        logger.error("The app is misconfigured or no JWT secret has been set")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    tokens, jwt_payload = ArxivUserClaims.unpack_token(token)
    while True:
        try:
            claims = ArxivUserClaims.decode_jwt_payload(tokens, jwt_payload, secret)
            return claims
        except jwcrypto.jwt.JWTExpired:
            if 'refresh' in tokens:
                # idp: ArxivOidcIdpClient = request.app.extra['idp']
                #  claims = idp.refresh_access_token(tokens['refresh'])
                #return claims
                raise AccessTokenExpired()

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        except jwcrypto.jwt.JWTInvalidClaimFormat:
            logger.warning(f"Chowed cookie '{token}'")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        except jwt.DecodeError:
            logger.warning(f"Chowed cookie '{token}'")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        except Exception as exc:
            logger.warning(f"token {token} is wrong?", exc_info=exc)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def get_db():
    """Dependency for fastapi routes"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def transaction():
    logger = getLogger(__name__)
    db = SessionLocal()
    try:
        yield db

        if db.new or db.dirty or db.deleted:
            db.commit()
    except Exception as e:
        logger.warning(f'Commit failed, rolling back', exc_info=1)
        db.rollback()
        raise
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
