"""Provides integration for the external user interface."""
import urllib.parse

from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import RedirectResponse, Response, JSONResponse

from arxiv.base import logging
from arxiv.auth.user_claims import ArxivUserClaims
from arxiv.auth.openid.oidc_idp import ArxivOidcIdpClient
from arxiv.auth.user_claims_to_legacy import create_tapir_session_from_user_claims
from arxiv.auth.legacy.sessions import invalidate as legacy_invalidate


from . import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get('/login')
def login(request: Request) -> Response:
    """User can log in with username and password, or permanent token."""
    # redirect to IdP
    idp: ArxivOidcIdpClient = request.app.extra["idp"]
    url = idp.login_url
    next_page = request.query_params.get('next_page', request.query_params.get('next', '/'))
    if next_page:
        url = url + "&state=" + urllib.parse.quote(next_page)
    logger.info(f"Login URL: {url}")
    return RedirectResponse(url)


@router.get('/callback')
def oauth2_callback(request: Request) -> Response:
    """User can log in with username and password, or permanent token."""
    code = request.query_params.get('code')
    if code is None:
        logger.warning("error: %s", repr(request.query_params))
        request.session.clear()
        return Response(status_code=status.HTTP_200_OK)

    idp: ArxivOidcIdpClient = request.app.extra["idp"]
    user_claims: ArxivUserClaims = idp.from_code_to_user_claims(code)

    if user_claims is None:
        logger.warning("Getting user claim failed. code: %s", repr(code))
        request.session.clear()
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    session_cookie_key = request.app.extra['AUTH_SESSION_COOKIE_NAME']
    classic_cookie_key = request.app.extra['CLASSIC_COOKIE_NAME']

    next_page = urllib.parse.unquote(request.query_params.get("state", "/"))  # Default to root if not provided
    logger.debug("callback success: next page: %s", next_page)
    response: Response = RedirectResponse(next_page, status_code=status.HTTP_303_SEE_OTHER)

    # NG cookie
    secret = request.app.extra['JWT_SECRET']
    token = user_claims.encode_jwt_token(secret)
    response.set_cookie(session_cookie_key, token, max_age=3600, samesite="lax")

    # legacy cookie
    try:
        tapir_cookie = create_tapir_session_from_user_claims(user_claims)
        response.set_cookie(classic_cookie_key, tapir_cookie, max_age=3600, samesite="lax")
    except Exception as exc:
        logger.error("Setting up Tapir session failed.", exc_info=exc)
        pass
    return response


@router.get('/logout')
def logout(request: Request, current_user: dict = Depends(get_current_user)) -> Response:
    """Log out of arXiv."""
    default_next_page = request.app.extra['LOGOUT_REDIRECT_URL']
    next_page = request.query_params.get('next_page', default_next_page)
    response = RedirectResponse(next_page, status_code=status.HTTP_303_SEE_OTHER)
    session_cookie_key = request.app.extra['AUTH_SESSION_COOKIE_NAME']
    legacy_cookie_key = request.app.extra['CLASSIC_COOKIE_NAME']

    if current_user is not None:
        logger.debug('Request to log out, then redirect to %s', next_page)
        idp: ArxivOidcIdpClient = request.app.extra["idp"]
        if not idp.logout_user(current_user):
            # Failed to log out, so keep the cookies
            return response

    response.set_cookie(session_cookie_key, "", max_age=0)

    #
    classic_cookie = request.cookies.get(legacy_cookie_key)
    try:
        legacy_invalidate(classic_cookie)
        response.set_cookie(legacy_cookie_key, "", max_age=0)
    except Exception as exc:
        logger.error("Setting up legacy session failed.", exc_info=exc)
        pass

    return response


@router.get('/token-names')
def logout(request: Request) -> JSONResponse:
    session_cookie_key = request.app.extra['AUTH_SESSION_COOKIE_NAME']
    classic_cookie_key = request.app.extra['CLASSIC_COOKIE_NAME']
    return {
        "session": session_cookie_key,
        "classic": classic_cookie_key
    }