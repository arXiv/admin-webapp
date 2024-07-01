"""Flask configuration."""
from typing import Optional, List, Tuple
import re
from arxiv.config import Settings as BaseSettings

class Settings (BaseSettings):

    BASE_SERVER: str = "arxiv.org"
    SERVER_NAME: str = BASE_SERVER

    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 7000
    REDIS_DATABASE: str = '0'
    REDIS_TOKEN: Optional[str] = None
    """This is the token used in the AUTH procedure."""
    REDIS_CLUSTER: bool = True

    REDIS_FAKE: bool = False
    """Use the FakeRedis library instead of a redis service.

    Useful for testing, dev, beta."""

    JWT_SECRET: str = 'foosecret'

    DEFAULT_LOGIN_REDIRECT_URL: str = 'https://arxiv.org/user'
    DEFAULT_LOGOUT_REDIRECT_URL: str = 'https://arxiv.org'

    LOGIN_REDIRECT_REGEX: str = fr'(/.*)|(https://([a-zA-Z0-9\-.])*{re.escape(BASE_SERVER)}/.*)'
    """Regex to check next_page of /login.

    Only next_page values that match this regex will be allowed. All
    others will go to the DEFAULT_LOGOUT_REDIRECT_URL. The default value
    for this allows relative URLs and URLs to subdomains of the
    BASE_SERVER.
    """
    URLS: List[Tuple[str, str, str]] = [
        ("lost_password", "/user/lost_password", BASE_SERVER),
        ("account", "/user", BASE_SERVER)
    ]      

    AUTH_SESSION_COOKIE_NAME: str = 'ARXIVNG_SESSION_ID'
    AUTH_SESSION_COOKIE_DOMAIN: str = '.arxiv.org'
    AUTH_SESSION_COOKIE_SECURE: bool = True

    CLASSIC_COOKIE_NAME: str = AUTH_SESSION_COOKIE_NAME
    CLASSIC_PERMANENT_COOKIE_NAME: str = 'tapir_permanent'

    CLASSIC_TRACKING_COOKIE: str = 'browser'
    CLASSIC_TOKEN_RECOVERY_TIMEOUT: int = 86400
    
    CLASSIC_SESSION_HASH: str = 'foosecret'
    SESSION_DURATION: int = 36000

    CAPTCHA_SECRET: str = 'foocaptcha'
    """Used to encrypt captcha answers, so that we don't need to store them."""

    CAPTCHA_FONT: Optional[str] = None

    CREATE_DB: bool = False

    AUTH_UPDATED_SESSION_REF: bool = True # see ARXIVNG-1920

    LOCALHOST_DEV: bool = False
    """Enables a set of config vars that facilites development on localhost"""

    WTF_CSRF_ENABLED: bool = False
    """Enable CSRF.

    Do not disable in production."""

    WTF_CSRF_EXEMPT: str = 'admin_webapp.routes.ui.login,admin_webapp.routes.ui.logout'
    """Comma seperted list of views to not do CSRF protection on.

    Login and logout lack the setup for this."""

    # if LOCALHOST_DEV:
    #     # Don't want to setup redis just for local developers
    #     REDIS_FAKE=True
    #     FLASK_DEBUG=True
    #     DEBUG=True
    #     if not SQLALCHEMY_DATABASE_URI:
    #         # SQLALCHEMY_DATABASE_URI = 'sqlite:///../locahost_dev.db'
    #         SQLALCHEMY_DATABASE_URI='mysql+mysqldb://root:root@localhost:3306/arXiv'

    #         # CLASSIC_DATABASE_URI = SQLALCHEMY_DATABASE_URI

    #     DEFAULT_LOGIN_REDIRECT_URL='/protected'
    #     # Need to use this funny name where we have a DNS entry to 127.0.0.1
    #     # because browsers will reject cookie domains with fewer than 2 dots
    #     AUTH_SESSION_COOKIE_DOMAIN='localhost.arxiv.org'
    #     # Want to not conflict with any existing cookies for subdomains of arxiv.org
    #     # so give it a different name
    #     CLASSIC_COOKIE_NAME='LOCALHOST_DEV_admin_webapp_classic_cookie'
    #     # Don't want to use HTTPS for local dev
    #     AUTH_SESSION_COOKIE_SECURE=0
    #     # Redirect to relative pages instead of arxiv.org pages
    #     DEFAULT_LOGOUT_REDIRECT_URL='/login'
    #     DEFAULT_LOGIN_REDIRECT_URL='/protected'
