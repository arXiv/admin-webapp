"""Application factory for admin_webapp."""

import logging

from flask import Flask
from flask_s3 import FlaskS3

from arxiv.base import Base
from arxiv.base.middleware import wrap

from arxiv_auth import auth
from arxiv_auth.auth.middleware import AuthMiddleware
from arxiv_auth.auth.sessions import SessionStore
from arxiv_auth.legacy.util import init_app as legacy_init_app
from arxiv_auth.legacy.util import create_all as legacy_create_all

from .routes import ui

s3 = FlaskS3()

logger = logging.getLogger(__name__)

def change_loglevel(pkg:str, level):
    """change log leve on arxiv-base logging

    arxiv-base logging isn't quite right in that the handler levels
    don't get updated after they get intitialzied.

    Use this like in the create_web_app function:

        change_loglevel('arxiv_auth.auth', 'DEBUG')
        change_loglevel('admin_webapp.controllers.authentication', 'DEBUG')
        change_loglevel('admin_webapp.routes.ui', 'DEBUG')
    """
    logger = logging.getLogger(pkg)
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)

def create_web_app() -> Flask:
    """Initialize and configure the admin_webapp application."""
    app = Flask('admin_webapp')
    app.config.from_pyfile('config.py')

    change_loglevel('arxiv_auth.auth', 'DEBUG')
    change_loglevel('admin_webapp.controllers.authentication', 'DEBUG')
    change_loglevel('admin_webapp.routes.ui', 'DEBUG')

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

    SessionStore.init_app(app)
    legacy_init_app(app)

    app.register_blueprint(ui.blueprint)
    Base(app)
    auth.Auth(app)
    s3.init_app(app)

    wrap(app, [AuthMiddleware])


    if not app.config['SQLALCHEMY_DATABASE_URI'] and not app.config['DEBUG']:
        logger.error("SQLALCHEMY_DATABASE_URI is not set!")

    if app.config['CREATE_DB']:
        with app.app_context():
            print("About to create the legacy DB")
            legacy_create_all()

    return app
