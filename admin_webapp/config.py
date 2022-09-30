"""Flask configuration."""

import os
import re


BASE_SERVER = os.environ.get('BASE_SERVER', 'arxiv.org')

SECRET_KEY = os.environ.get('SECRET_KEY', 'asdf1234')
"""SECRET_KEY used for flask sessions."""

SESSION_COOKIE_PATH = os.environ.get('APPLICATION_ROOT', '/')

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '7000')
REDIS_DATABASE = os.environ.get('REDIS_DATABASE', '0')
REDIS_TOKEN = os.environ.get('REDIS_TOKEN', None)
"""This is the token used in the AUTH procedure."""
REDIS_CLUSTER = os.environ.get('REDIS_CLUSTER', '1')

REDIS_FAKE = os.environ.get('REDIS_FAKE', False)
"""Use the FakeRedis library instead of a redis service.

Useful for testing, dev, beta."""

JWT_SECRET = os.environ.get('JWT_SECRET', 'foosecret')

DEFAULT_LOGIN_REDIRECT_URL = os.environ.get(
    'DEFAULT_LOGIN_REDIRECT_URL',
    'https://arxiv.org/user'
)
DEFAULT_LOGOUT_REDIRECT_URL = os.environ.get(
    'DEFAULT_LOGOUT_REDIRECT_URL',
    'https://arxiv.org'
)

LOGIN_REDIRECT_REGEX = os.environ.get('LOGIN_REDIRECT_REGEX',
                                      fr'(/.*)|(https://([a-zA-Z0-9\-.])*{re.escape(BASE_SERVER)}/.*)')
"""Regex to check next_page of /login.

Only next_page values that match this regex will be allowed. All
others will go to the DEFAULT_LOGOUT_REDIRECT_URL. The default value
for this allows relative URLs and URLs to subdomains of the
BASE_SERVER.
"""

login_redirect_pattern = re.compile(LOGIN_REDIRECT_REGEX)

AUTH_SESSION_COOKIE_NAME = 'ARXIVNG_SESSION_ID'
AUTH_SESSION_COOKIE_DOMAIN = os.environ.get('AUTH_SESSION_COOKIE_DOMAIN', '.arxiv.org')
AUTH_SESSION_COOKIE_SECURE = bool(int(os.environ.get('AUTH_SESSION_COOKIE_SECURE', '1')))

CLASSIC_COOKIE_NAME = os.environ.get('CLASSIC_COOKIE_NAME', 'tapir_session')
CLASSIC_PERMANENT_COOKIE_NAME = os.environ.get(
    'CLASSIC_PERMANENT_COOKIE_NAME',
    'tapir_permanent'
)
CLASSIC_TRACKING_COOKIE = os.environ.get('CLASSIC_TRACKING_COOKIE', 'browser')
CLASSIC_TOKEN_RECOVERY_TIMEOUT = os.environ.get(
    'CLASSIC_TOKEN_RECOVERY_TIMEOUT',
    '86400'
)
CLASSIC_SESSION_HASH = os.environ.get('CLASSIC_SESSION_HASH', 'foosecret')
SESSION_DURATION = os.environ.get(
    'SESSION_DURATION',
    '36000'
)

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False

CAPTCHA_SECRET = os.environ.get('CAPTCHA_SECRET', 'foocaptcha')
"""Used to encrypt captcha answers, so that we don't need to store them."""

CAPTCHA_FONT = os.environ.get('CAPTCHA_FONT', None)

URLS = [
    ("lost_password", "/user/lost_password", BASE_SERVER),
    ("account", "/user", BASE_SERVER)
]

CREATE_DB = bool(int(os.environ.get('CREATE_DB', 0)))


AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'nope')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', 'nope')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
FLASKS3_BUCKET_NAME = os.environ.get('FLASKS3_BUCKET_NAME', 'some_bucket')
FLASKS3_CDN_DOMAIN = os.environ.get('FLASKS3_CDN_DOMAIN', 'static.arxiv.org')
FLASKS3_USE_HTTPS = os.environ.get('FLASKS3_USE_HTTPS', 1)
FLASKS3_FORCE_MIMETYPE = os.environ.get('FLASKS3_FORCE_MIMETYPE', 1)
FLASKS3_ACTIVE = os.environ.get('FLASKS3_ACTIVE', 0)
"""Flask-S3 plugin settings."""

AUTH_UPDATED_SESSION_REF = True # see ARXIVNG-1920

LOCALHOST_DEV = os.environ.get('LOCALHOST_DEV', False)
"""Enables a set of config vars that facilites development on localhost"""

if LOCALHOST_DEV:
    # Don't want to setup redis just for local developers
    REDIS_FAKE=True
    FLASK_DEBUG=True
    DEBUG=True
    if not SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///../locahost_dev.db'

    DEFAULT_LOGIN_REDIRECT_URL='/protected'
    # Need to use this funny name where we have a DNS entry to 127.0.0.1
    # because browsers will reject cookie domains with fewer than 2 dots
    AUTH_SESSION_COOKIE_DOMAIN='localhost.arxiv.org'
    # Want to not conflict with any existing cookies for subdomains of arxiv.org
    # so give it a different name
    CLASSIC_COOKIE_NAME='LOCALHOST_DEV_admin_webapp_classic_cookie'
    # Don't want to use HTTPS for local dev
    AUTH_SESSION_COOKIE_SECURE=0
    # Redirect to relative pages instead of arxiv.org pages
    DEFAULT_LOGOUT_REDIRECT_URL='/login'
    DEFAULT_LOGIN_REDIRECT_URL='/protected'
