import os
from typing import Callable
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import Response, RedirectResponse

# from admin_api_routes.authentication import router as auth_router
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
from admin_api_routes.user import router as user_router
from admin_api_routes.tapir_sessions import router as tapir_session_router

from admin_api_routes.frontend import router as frontend_router


from arxiv.base.logging import getLogger

from arxiv.config import Settings
from arxiv.db.models import configure_db
from arxiv.auth.openid.oidc_idp import ArxivOidcIdpClient

from app_logging import setup_logger

# Keycloak server url
KEYCLOAK_SERVER_URL = os.environ.get('KEYCLOAK_SERVER_URL', 'http://127.0.0.1:3033')
# arxiv-user client secret
KEYCLOAK_CLIENT_SECRET = os.environ.get("KEYCLOAK_CLIENT_SECRET", "foo")
#
DB_URI = os.environ.get('CLASSIC_DB_URI')
#
#
AAA_CALLBACK_URL = os.environ.get("AAA_CALLBACK_URL", "http://127.0.0.1:5000/aaa/callback")
#
AAA_LOGIN_REDIRECT_URL = os.environ.get("AAA_LOGIN_REDIRECT_URL", "http://127.0.0.1:5000/aaa/login")
#
LOGOUT_REDIRECT_URL = os.environ.get("LOGOUT_REDIRECT_URL", "http://127.0.0.1:5000")

_idp_ = ArxivOidcIdpClient(AAA_CALLBACK_URL,
                           scope=["openid"],
                           server_url=KEYCLOAK_SERVER_URL,
                           client_secret=KEYCLOAK_CLIENT_SECRET,
                           logger=getLogger(__name__)
                           )

origins = [
    "http://127.0.0.1",
    "http://localhost",
    "http://127.0.0.1:5000/aaa",
    "http://localhost:5000/aaa",
    "http://127.0.0.1:4042",
    "http://localhost:4042",
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
    engine, _ = configure_db(settings)

    app = FastAPI(
        root_path="/api",
        idp=_idp_,
        arxiv_db_engine=engine,
        arxiv_settings=settings,
        JWT_SECRET=settings.SECRET_KEY,
        LOGIN_REDIRECT_URL=AAA_LOGIN_REDIRECT_URL,
        LOGOUT_REDIRECT_URL=LOGOUT_REDIRECT_URL,
        AUTH_SESSION_COOKIE_NAME="arxiv_session_cookie",
        CLASSIC_COOKIE_NAME="tapir_session_cookie",
    )

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

    return app