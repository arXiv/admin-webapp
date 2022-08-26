"""Provides Flask integration for the external user interface."""

from typing import Any, Callable
from datetime import datetime, timedelta
from functools import wraps
from pytz import timezone, UTC
from flask import Blueprint, render_template, url_for, request, \
    make_response, redirect, current_app, send_file, Response

from arxiv import status
from arxiv_auth import domain
from arxiv.base import logging

from ..controllers import captcha_image, registration, authentication


logger = logging.getLogger(__name__)
blueprint = Blueprint('ui', __name__, url_prefix='')

def anonymous_only(func: Callable) -> Callable:
    """Redirect logged-in users to their profile."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if hasattr(request, 'auth') and request.auth:
            next_page = request.args.get('next_page',
                                         current_app.config['DEFAULT_LOGIN_REDIRECT_URL'])
            return make_response(redirect(next_page, code=status.HTTP_303_SEE_OTHER))
        else:
            return func(*args, **kwargs)
    return wrapper


def set_cookies(response: Response, data: dict) -> None:
    """
    Update a :class:`.Response` with cookies in controller data.

    Contollers seeking to update cookies must include a 'cookies' key
    in their response data.
    """
    # Set the session cookie.
    cookies = data.pop('cookies')
    if cookies is None:
        return None
    for cookie_key, (cookie_value, expires) in cookies.items():
        cookie_name = current_app.config[f'{cookie_key.upper()}_NAME']
        max_age = timedelta(seconds=expires)
        logger.debug('Set cookie %s with %s, max_age %s',
                     cookie_name, cookie_value, max_age)
        domain = current_app.config['AUTH_SESSION_COOKIE_DOMAIN']
        params = dict(httponly=True, domain=domain)
        if current_app.config['AUTH_SESSION_COOKIE_SECURE']:
            # Setting samesite to lax, to allow reasonable links to
            # authenticated views using GET requests.
            params.update({'secure': True, 'samesite': 'lax'})
        response.set_cookie(cookie_name, cookie_value, max_age=max_age,
                            **params)



@blueprint.after_request
def apply_response_headers(response: Response) -> Response:
    """Apply response headers to all responses."""
    """Prevent UI redress attacks."""
    response.headers['Content-Security-Policy'] = "frame-ancestors 'none'"
    response.headers['X-Frame-Options'] = 'DENY'

    return response

@blueprint.route('/register', methods=['GET', 'POST'])
@anonymous_only
def register() -> Response:
    """Interface for creating new accounts."""
    captcha_secret = current_app.config['CAPTCHA_SECRET']
    ip_address = request.remote_addr
    next_page = request.args.get('next_page', url_for('account'))
    data, code, headers = registration.register(request.method, request.form,
                                                captcha_secret, ip_address,
                                                next_page)

    # Flask puts cookie-setting methods on the response, so we do that here
    # instead of in the controller.
    if code is status.HTTP_303_SEE_OTHER:
        response = make_response(redirect(headers['Location'], code=code))
        set_cookies(response, data)
        return response
    content = render_template("register.html", **data)
    response = make_response(content, code, headers)
    return response


@blueprint.route('/login', methods=['GET', 'POST'])
@anonymous_only
def login() -> Response:
    """User can log in with username and password, or permanent token."""
    ip_address = request.remote_addr
    form_data = request.form
    default_next_page = current_app.config['DEFAULT_LOGIN_REDIRECT_URL']
    next_page = request.args.get('next_page', default_next_page)
    logger.debug('Request to log in, then redirect to %s', next_page)
    data, code, headers = authentication.login(request.method,
                                               form_data, ip_address,
                                               next_page)
    data.update({'pagetitle': 'Log in to arXiv'})
    # Flask puts cookie-setting methods on the response, so we do that here
    # instead of in the controller.
    if code is status.HTTP_303_SEE_OTHER:
        # Set the session cookie.
        response = make_response(redirect(headers.get('Location'), code=code))
        set_cookies(response, data)
        unset_submission_cookie(response)    # Fix for ARXIVNG-1149.
        return response

    # Form is invalid, or login failed.
    response = Response(
        render_template("login.html", **data),
        status=code
    )
    return response


@blueprint.route('/logout', methods=['GET'])
def logout() -> Response:
    """Log out of arXiv."""
    session_cookie_key = current_app.config['AUTH_SESSION_COOKIE_NAME']
    classic_cookie_key = current_app.config['CLASSIC_COOKIE_NAME']
    session_cookie = request.cookies.get(session_cookie_key, None)
    classic_cookie = request.cookies.get(classic_cookie_key, None)
    default_next_page = current_app.config['DEFAULT_LOGOUT_REDIRECT_URL']
    next_page = request.args.get('next_page', default_next_page)
    logger.debug('Request to log out, then redirect to %s', next_page)
    data, code, headers = authentication.logout(session_cookie, classic_cookie,
                                                next_page)
    # Flask puts cookie-setting methods on the response, so we do that here
    # instead of in the controller.
    if code is status.HTTP_303_SEE_OTHER:
        logger.debug('Redirecting to %s: %i', headers.get('Location'), code)
        response = make_response(redirect(headers.get('Location'), code=code))
        set_cookies(response, data)
        unset_submission_cookie(response)    # Fix for ARXIVNG-1149.
        # Partial fix for ARXIVNG-1653, ARXIVNG-1644
        unset_permanent_cookie(response)
        return response
    return redirect(next_page, code=status.HTTP_302_FOUND)


@blueprint.route('/captcha', methods=['GET'])
def captcha() -> Response:
    """Provide the image for stateless captcha."""
    secret = current_app.config['CAPTCHA_SECRET']
    font = current_app.config.get('CAPTCHA_FONT')
    token = request.args.get('token')
    data, code, headers = captcha_image.get(token, secret, request.remote_addr, font)
    return send_file(data['image'], mimetype=data['mimetype']), code, headers


@blueprint.route('/auth_status', methods=['GET'])
def auth_status() -> Response:
    """Get if the app is running."""
    return make_response("OK")
