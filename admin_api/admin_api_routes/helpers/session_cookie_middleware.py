from datetime import datetime, timezone

import httpx
from arxiv.auth.user_claims import ArxivUserClaims
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from admin_api_routes.authentication import logger


# Define custom middleware to add a cookie to the response
class SessionCookieMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        session_cookie_name = request.app.extra['AUTH_SESSION_COOKIE_NAME']
        classic_cookie_name = request.app.extra['CLASSIC_COOKIE_NAME']
        token = request.cookies.get(session_cookie_name)
        refreshed_tokens = None
        if token is not None:
            tokens, jwt_payload = ArxivUserClaims.unpack_token(token)
            expires_at = datetime.strptime(tokens['expires_at'], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc)
            remain = expires_at - datetime.now(timezone.utc)
            need_token_refresh = remain.total_seconds() < 180

            if need_token_refresh and 'refresh' in tokens:
                AAA_TOKEN_REFRESH_URL = request.app.extra['AAA_TOKEN_REFRESH_URL']
                cookies = request.cookies
                try:
                    async with httpx.AsyncClient() as client:
                        refresh_response = await client.post(
                            AAA_TOKEN_REFRESH_URL,
                            json={
                                "session": cookies.get(session_cookie_name),
                                "classic": cookies.get(classic_cookie_name),
                            },
                            cookies=cookies)

                    if refresh_response.status_code == 200:
                        # Extract the new token from the response
                        refreshed_tokens = await refresh_response.json()
                    else:
                        logger.warning("calling /fefresh failed. status = %s", refresh_response.status_code)
                except Exception as exc:
                    logger.warning("calling /fefresh failed.", exc_info=exc)
                    pass

        response = await call_next(request)
        if refreshed_tokens:
            new_session_cookie = refreshed_tokens.get("session")
            new_classic_cookie = refreshed_tokens.get("classic")
            max_age = refreshed_tokens.get("max_age")
            domain = refreshed_tokens.get("domain")
            secure = refreshed_tokens.get("secure")
            samesite = refreshed_tokens.get("samesite")
            response.set_cookie(session_cookie_name, new_session_cookie,
                                max_age=max_age, domain=domain, secure=secure, samesite=samesite)
            response.set_cookie(classic_cookie_name, new_classic_cookie,
                                max_age=max_age, domain=domain, secure=secure, samesite=samesite)


        return response
