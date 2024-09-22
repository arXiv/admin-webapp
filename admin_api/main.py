import logging
import os
import httpx
from typing import Callable
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import Response, RedirectResponse, JSONResponse

from arxiv.base.globals import get_application_config

from admin_api_routes import AccessTokenExpired, LoginRequired, BadCookie
# from admin_api_routes.authentication import router as auth_router
from admin_api_routes.admin_logs import router as admin_log_router
from admin_api_routes.categories import router as categories_router
from admin_api_routes.email_template import router as email_template_router
from admin_api_routes.endorsement_requsets import router as endorsement_request_router
from admin_api_routes.endorsement_requsets_audit import router as endorsement_request_audit_router
from admin_api_routes.endorsements import router as endorsement_router
from admin_api_routes.demographic import router as demographic_router
from admin_api_routes.documents import router as document_router
from admin_api_routes.moderators import router as moderator_router
from admin_api_routes.ownership_requests import router as ownership_request_router
from admin_api_routes.ownership_requests_audit import router as ownership_request_audit_router
from admin_api_routes.paper_owners import router as ownership_router
from admin_api_routes.submissions import router as submission_router, meta_router as submission_meta_router
from admin_api_routes.user import router as user_router
from admin_api_routes.tapir_sessions import router as tapir_session_router

from admin_api_routes.frontend import router as frontend_router


from arxiv.base.logging import getLogger

from arxiv.config import Settings

from app_logging import setup_logger

# API root path (excluding the host)
ADMIN_API_ROOT_PATH = os.environ.get('ADMIN_API_ROOT_PATH', '/adminapi')

# Admin app URL
#
ADMIN_APP_URL = os.environ.get('ADMIN_APP_URL', 'http://localhost.arxiv.org:5000/admin-console')
#
DB_URI = os.environ.get('CLASSIC_DB_URI')
#
#
#
AAA_LOGIN_REDIRECT_URL = os.environ.get("AAA_LOGIN_REDIRECT_URL", "http://localhost.arxiv.org:5000/aaa/login")
# When it got the expired, ask the oauth server to refresh the token
# This is still WIP.
AAA_TOKEN_REFRESH_URL = os.environ.get("AAA_TOKEN_REFRESH_URL", "http://localhost.arxiv.org:5000/aaa/refresh")
#
LOGOUT_REDIRECT_URL = os.environ.get("LOGOUT_REDIRECT_URL", ADMIN_APP_URL)
#
JWT_SECRET = os.environ.get("JWT_SECRET")
AUTH_SESSION_COOKIE_NAME = os.environ.get("AUTH_SESSION_COOKIE_NAME", "arxiv_oidc_session")
CLASSIC_COOKIE_NAME = os.environ.get("CLASSIC_COOKIE_NAME", "tapir_session")

SQLALCHMEY_MAPPING = {
    'pool_size': 8,
    'max_overflow': 8,
    'pool_timeout': 30,
    'pool_recycle': 900
}

# Auth is now handled by auth service
# No need for keycloak URL, etc.

origins = [
    "http://localhost",
    "http://localhost/",
    "http://localhost:5000",
    "http://localhost:5000/",
    "http://localhost:5000/admin-console",
    "http://localhost:5000/admin-console/",
    "https://dev3.arxiv.org",
    "https://dev3.arxiv.org/",
    "https://dev.arxiv.org",
    "https://dev.arxiv.org/",
    "https://arxiv.org",
    "https://arxiv.org/"
]

class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Log request details
        body = await request.body()
        print(f"Request: {request.method} {request.url}")
        print(f"Request Headers: {request.headers}")
        print(f"Request Body: {body.decode('utf-8')}")

        # Call the next middleware or endpoint
        response = await call_next(request)

        # Capture response body
        response_body = [section async for section in response.body_iterator]
        response.body_iterator = iter(response_body)
        response_body_str = b''.join(response_body).decode('utf-8')

        # Log response details
        print(f"Response: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Body: {response_body_str}")

        return response

def create_app(*args, **kwargs) -> FastAPI:
    setup_logger()

    settings = Settings (
        CLASSIC_DB_URI = DB_URI,
        LATEXML_DB_URI = None
    )
    from arxiv.db import init as arxiv_db_init, _classic_engine
    arxiv_db_init(settings)

    jwt_secret = get_application_config().get('JWT_SECRET', settings.SECRET_KEY)

    app = FastAPI(
        root_path=ADMIN_API_ROOT_PATH,
        arxiv_db_engine=_classic_engine,
        arxiv_settings=settings,
        JWT_SECRET=jwt_secret,
        LOGIN_REDIRECT_URL=AAA_LOGIN_REDIRECT_URL,
        LOGOUT_REDIRECT_URL=LOGOUT_REDIRECT_URL,
        AUTH_SESSION_COOKIE_NAME=AUTH_SESSION_COOKIE_NAME,
        CLASSIC_COOKIE_NAME=CLASSIC_COOKIE_NAME,
    )

    if ADMIN_APP_URL not in origins:
        origins.append(ADMIN_APP_URL)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # app.add_middleware(LogMiddleware)
    app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")

    # app.include_router(auth_router)
    app.include_router(admin_log_router, prefix="/v1")
    app.include_router(categories_router, prefix="/v1")
    app.include_router(demographic_router, prefix="/v1")
    app.include_router(user_router, prefix="/v1")
    app.include_router(email_template_router, prefix="/v1")
    app.include_router(endorsement_router, prefix="/v1")
    app.include_router(endorsement_request_router, prefix="/v1")
    app.include_router(endorsement_request_audit_router, prefix="/v1")
    app.include_router(ownership_request_router, prefix="/v1")
    app.include_router(ownership_request_audit_router, prefix="/v1")
    app.include_router(moderator_router, prefix="/v1")
    app.include_router(document_router, prefix="/v1")
    app.include_router(ownership_router, prefix="/v1")
    app.include_router(submission_router, prefix="/v1")
    app.include_router(submission_meta_router, prefix="/v1")
    app.include_router(tapir_session_router, prefix="/v1")
    app.include_router(frontend_router)

    @app.middleware("http")
    async def apply_response_headers(request: Request, call_next: Callable) -> Response:
        """Apply response headers to all responses.
           Prevent UI redress attacks.
        """
        response: Response = await call_next(request)
        response.headers['Content-Security-Policy'] = "frame-ancestors 'none'"
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @app.get("/")
    async def root(request: Request):
        return RedirectResponse("/frontend")

    @app.exception_handler(AccessTokenExpired)
    async def user_not_authenticated_exception_handler(request: Request,
                                                       _exc: AccessTokenExpired):
        logger = logging.getLogger(__name__)
        original_url = str(request.url)
        logger.info('Access token expired %s', original_url)
        cookie_name = request.app.extra['AUTH_SESSION_COOKIE_NAME']
        classic_cookie_name = request.app.extra['CLASSIC_COOKIE_NAME']

        cookies = request.cookies
        try:
            async with httpx.AsyncClient() as client:
                refresh_response = await client.post(
                    AAA_TOKEN_REFRESH_URL,
                    data={
                        "session": cookies.get(cookie_name),
                        "classic": cookies.get(classic_cookie_name),
                    },
                    cookies=cookies)

            if refresh_response.status_code != 200:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "Failed to refresh access token"}
                )
            # Extract the new token from the response
            refreshed_tokens = await refresh_response.json()
            new_session_cookie = refreshed_tokens.get("session")
            new_classic_cookie = refreshed_tokens.get("classic")
            max_age = refreshed_tokens.get("max_age")
            domain = refreshed_tokens.get("domain")
            secure = refreshed_tokens.get("secure")
            samesite = refreshed_tokens.get("samesite")
            # Step 3: Redirect back to the original URL and set the new cookie
            response = RedirectResponse(url=original_url, status_code=status.HTTP_302_FOUND)
            response.set_cookie(cookie_name, new_session_cookie,
                                max_age=max_age, domain=domain, secure=secure, samesite=samesite)
            response.set_cookie(classic_cookie_name, new_classic_cookie,
                                max_age=max_age, domain=domain, secure=secure, samesite=samesite)
            return response

        except Exception as _exc:
            logger.warning("Failed to refresh access token: %s", _exc)
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "Failed to refresh access token"}
            )

    @app.exception_handler(LoginRequired)
    async def login_required_exception_handler(request: Request,
                                               _exc: LoginRequired):
        logger = logging.getLogger(__name__)
        original_url = str(request.url)
        login_url = f"{AAA_LOGIN_REDIRECT_URL}?next_page={original_url}"
        logger.info('Login required %s -> %s ', original_url, login_url)
        #return RedirectResponse(url=login_url, status_code=status.HTTP_302_FOUND)
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    @app.exception_handler(BadCookie)
    async def bad_cookie_exception_handler(request: Request,
                                           _exc: BadCookie):
        logger = logging.getLogger(__name__)
        original_url = str(request.url)
        login_url = f"{AAA_LOGIN_REDIRECT_URL}?next_page={original_url}"
        logger.info('Bad cookie %s -> %s ', original_url, login_url)
        return RedirectResponse(url=login_url, status_code=status.HTTP_302_FOUND)

    return app
