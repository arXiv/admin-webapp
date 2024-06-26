"""Application factory for admin_webapp."""

import logging

from flask import Flask
from flask_session import Session
from flask_bootstrap import Bootstrap5

from flask_wtf.csrf import CSRFProtect

from arxiv.base import Base
from arxiv.base.middleware import wrap
from arxiv.db.models import configure_db
from arxiv.auth import auth
from arxiv.auth.auth.middleware import AuthMiddleware
from arxiv.auth.legacy.util import create_all as legacy_create_all

from . import filters
from .config import Settings
from .routes import ui, ownership, endorsement, user, paper

logger = logging.getLogger(__name__)

csrf = CSRFProtect()

def change_loglevel(pkg:str, level):
    """Change log leve on arxiv-base logging.

    arxiv-base logging isn't quite right in that the handler levels
    don't get updated after they get intitialzied.

    Use this like in the create_web_app function:

        change_loglevel('arxiv_auth.auth', 'DEBUG')
        change_loglevel('admin_webapp.controllers.authentication', 'DEBUG')
        change_loglevel('admin_webapp.routes.ui', 'DEBUG')
    """
    logger_x = logging.getLogger(pkg)
    logger_x.setLevel(level)
    for handler in logger_x.handlers:
        handler.setLevel(level)

def create_web_app(**kwargs) -> Flask:
    """Initialize and configure the admin_webapp application."""
    app = Flask('admin_webapp')
    settings = Settings(**kwargs)
    app.config.from_object(settings)
    app.engine, _  = configure_db(settings)
    session_lifetime = app.config['PERMANENT_SESSION_LIFETIME']

    print(f"Session Lifetime: {session_lifetime} seconds")
    # Configure Flask session (use filesystem for dev purposes)
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)
    Bootstrap5(app)

    # change_loglevel('arxiv_auth.legacy.authenticate', 'DEBUG')
    # change_loglevel('arxiv_auth.auth', 'DEBUG')
    # change_loglevel('arxiv_auth.auth.decorator', 'DEBUG')
    # change_loglevel('arxiv_auth.legacy.util', 'DEBUG')

    # change_loglevel('admin_webapp.controllers.authentication', 'DEBUG')
    # change_loglevel('admin_webapp.routes.ui', 'DEBUG')

    # Don't set SERVER_NAME, it switches flask blueprints to be
    # subdomain aware.  Then each blueprint will only be served on
    # it's subdomain.  This doesn't work with mutliple domains like
    # webN.arxiv.org and arxiv.org. We need to handle both names so
    # that individual nodes can be addresed for diagnotics. Not
    # setting this will allow the flask app to handle both
    # https://web3.arxiv.org/login and https://arxiv.org/login. If
    # this gets set paths that should get handled by the app will 404
    # when the request is made with a HOST that doesn't match
    # SERVER_NAME.
    app.config['SERVER_NAME'] = None

    app.register_blueprint(ui.blueprint)
    app.register_blueprint(ownership.blueprint)
    app.register_blueprint(endorsement.blueprint)
    app.register_blueprint(user.blueprint)
    app.register_blueprint(paper.blueprint)

    Base(app)
    auth.Auth(app)

    csrf.init_app(app)
    [csrf.exempt(view.strip())
     for view in app.config['WTF_CSRF_EXEMPT'].split(',')]

    wrap(app, [AuthMiddleware])

    setup_warnings(app)

    app.jinja_env.filters['unix_to_datetime'] = filters.unix_to_datetime

    if app.config['CREATE_DB']:
        print ("CREATED DB")
        legacy_create_all(app.engine)

    return app


def setup_warnings(app):
    if not app.config.get('WTF_CSRF_ENABLED'):
        logger.warning("CSRF protection is DISABLED, Do not disable CSRF in production")
