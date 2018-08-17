"""Flask configuration."""

import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'asdf1234')
SERVER_NAME = os.environ.get('REGISTRY_SERVER_NAME')

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'nope')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', 'nope')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')

LOGFILE = os.environ.get('LOGFILE')
LOGLEVEL = os.environ.get('LOGLEVEL', 20)

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
REDIS_DATABASE = os.environ.get('REDIS_DATABASE', '0')
REDIS_TOKEN = os.environ.get('REDIS_TOKEN', None)
"""This is the token used in the AUTH procedure."""


JWT_SECRET = os.environ.get('JWT_SECRET', 'foosecret')

DEFAULT_LOGIN_REDIRECT_URL = os.environ.get(
    'DEFAULT_LOGIN_REDIRECT_URL',
    'https://arxiv.org/user'
)
DEFAULT_LOGOUT_REDIRECT_URL = os.environ.get(
    'DEFAULT_LOGOUT_REDIRECT_URL',
    'https://arxiv.org'
)

SESSION_COOKIE_NAME = 'ARXIVNG_SESSION_ID'
SESSION_COOKIE_SECURE = bool(int(os.environ.get('SESSION_COOKIE_SECURE', '1')))

EXTERNAL_URL_SCHEME = os.environ.get('EXTERNAL_URL_SCHEME', 'https')
BASE_SERVER = os.environ.get('BASE_SERVER', 'arxiv.org')
URLS = [
    ("register", "/register", BASE_SERVER),
    ("lost_password", "/lost_password", BASE_SERVER),
]

REGISTRY_DATABASE_URI = os.environ.get('REGISTRY_DATABASE_URI', 'sqlite://')