"""Provides integration for the external user interface."""
import urllib.parse
import requests

from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import RedirectResponse, Response, JSONResponse

from arxiv.base import logging
from arxiv.auth.user_claims import ArxivUserClaims
from arxiv.auth.openid.oidc_idp import ArxivOidcIdpClient

from . import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get('/login')
def login(request: Request) -> Response:
    """User can log in with username and password, or permanent token."""
    # redirect to IdP
    idp: ArxivOidcIdpClient = request.app.extra["idp"]
    next_page = request.query_params.get('next_page', request.query_params.get('next', '/'))
    if next_page:
        next_page = "?state=" + next_page
    return RedirectResponse(idp.login_url + next_page)


@router.get('/callback')
def oauth2_callback(request: Request) -> Response:
    """User can log in with username and password, or permanent token."""
    code = request.query_params.get('code')
    idp: ArxivOidcIdpClient = request.app.extra["idp"]
    user_claims = idp.from_code_to_user_claims(code)

    if user_claims is None:
        request.session.clear()
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    session_cookie_key = request.app.extra['AUTH_SESSION_COOKIE_NAME']
    classic_cookie_key = request.app.extra['CLASSIC_COOKIE_NAME']
    secret = request.app.extra['JWT_SECRET']

    token = user_claims.encode_jwt_token(secret)
    # next_page = urllib.parse.unquote(request.query_params.get("state", "/"))  # Default to root if not provided
    next_page = "http://127.0.0.1:5000/users"
    response: Response = RedirectResponse(next_page, status_code=status.HTTP_303_SEE_OTHER) if next_page else Response(status_code=status.HTTP_200_OK)
    response.set_cookie(session_cookie_key, token, max_age=3600)
    response.set_cookie("token", session_cookie_key, max_age=3600)
    # response.set_cookie(classic_cookie_key, user_claims.to_arxiv_token_string, max_age=3600)

    ui_response = requests.get(idp.user_info_url,
                               headers={"Authorization": "Bearer {}".format(user_claims._claims['access_token'])})
    return response


@router.get('/logout')
def logout(request: Request, response: Response, current_user: dict = Depends(get_current_user)) -> Response:
    """Log out of arXiv."""
    session_cookie_key = request.app.extra['AUTH_SESSION_COOKIE_NAME']
    classic_cookie_key = request.app.extra['CLASSIC_COOKIE_NAME']

    default_next_page = request.app.extra['LOGOUT_REDIRECT_URL']
    next_page = request.query_params.get('next_page', default_next_page)
    logger.debug('Request to log out, then redirect to %s', next_page)


    user_cookie = request.cookies.get(session_cookie_key)
    if user_cookie:
        secret = request.app.extra['JWT_SECRET']
        user = ArxivUserClaims.decode_jwt_token(user_cookie, secret)
        if user:
            idp: ArxivOidcIdpClient = request.app.extra["idp"]
            if idp.logout_user(user):
                response.set_cookie(session_cookie_key, max_age=0)
                response.set_cookie("token", max_age=0)
                response.set_cookie(classic_cookie_key, max_age=0)
                response.set_cookie("submit_session", max_age=0)

    return RedirectResponse(next_page, status_code=status.HTTP_303_SEE_OTHER)


@router.get('/token-names')
def logout(request: Request) -> JSONResponse:
    session_cookie_key = request.app.extra['AUTH_SESSION_COOKIE_NAME']
    classic_cookie_key = request.app.extra['CLASSIC_COOKIE_NAME']
    return {
        "session": session_cookie_key,
        "classic": classic_cookie_key
    }
