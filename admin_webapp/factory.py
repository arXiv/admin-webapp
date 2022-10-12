"""Application factory for admin_webapp."""

import logging

from flask import Flask
from flask_s3 import FlaskS3
from flask_bootstrap import Bootstrap5

from flask_wtf.csrf import CSRFProtect

from arxiv.base import Base
from arxiv.base.middleware import wrap

from arxiv_auth import auth
from arxiv_auth.auth.middleware import AuthMiddleware
from arxiv_auth.auth.sessions import SessionStore
from arxiv_auth.legacy.util import init_app as legacy_init_app
#from arxiv_auth.legacy.util import create_all as legacy_create_all

from flask_sqlalchemy import SQLAlchemy

import arxiv_db

from .routes import ui, ownership, endorsement, user, paper, tapir_session

s3 = FlaskS3()

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

def create_web_app() -> Flask:
    """Initialize and configure the admin_webapp application."""
    app = Flask('admin_webapp')
    app.config.from_pyfile('config.py')

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

    SessionStore.init_app(app)
    legacy_init_app(app)

    db = SQLAlchemy(app, metadata=arxiv_db.Base.metadata)

    app.register_blueprint(ui.blueprint)
    app.register_blueprint(ownership.blueprint)
    app.register_blueprint(endorsement.blueprint)
    app.register_blueprint(user.blueprint)
    app.register_blueprint(paper.blueprint)
    app.register_blueprint(tapir_session.blueprint)

    Base(app)
    auth.Auth(app)
    s3.init_app(app)

    csrf.init_app(app)
    [csrf.exempt(view.strip())
     for view in app.config['WTF_CSRF_EXEMPT'].split(',')]

    wrap(app, [AuthMiddleware])

    _settup_warnings(app)

    if app.config['CREATE_DB']:
        with app.app_context():
            print("About to create the legacy DB")
            #legacy_create_all()
            from datetime import datetime, timedelta
            from sqlalchemy.orm import Session
            from sqlalchemy import insert, select
            from flask import url_for
            from arxiv_db.models import Endorsements, EndorsementRequests, Demographics, TapirUsers
            from .extensions import get_db
            from arxiv_db import test_load_db_file, models
            from arxiv_db.tables import arxiv_tables
            arxiv_tables.metadata.create_all(bind=db.engine)

            session = db.session
            SQL_DATA_FILE = './tests/data/data.sql'
            test_load_db_file(db.engine, SQL_DATA_FILE)
            endorser = TapirUsers(first_name='Sally', last_name='LongCareer', policy_class=2, email='slc234@cornell.edu')
            session.add(endorser)
            endorsee = TapirUsers(first_name='Aspen', last_name='Early', policy_class=2, email='ase12@cornell.edu')
            session.add(endorsee)
            endorsee_sus = TapirUsers(first_name='Bobby', last_name='NoPapers', policy_class=2, email='bob@scamy.example.com')
            endorsee_sus.demographics = Demographics(flag_suspect=1, archive='cs', subject_class='CR')
            session.add(endorsee_sus)

            req1 = EndorsementRequests(endorsee=endorsee,
                                    secret='end_sec_0',
                                    archive='cs', subject_class='CR',
                                    issued_when=datetime.now(),
                                    flag_valid=1, point_value=10)
            req1.endorsement = Endorsements(endorser=endorser, endorsee=endorsee,                                     archive='cs', subject_class='CR',)

            req2 = EndorsementRequests(endorsee=endorsee_sus,
                                    secret='end_sec_1',
                                    archive='cs', subject_class='CR',
                                    issued_when=datetime.now(),
                                    flag_valid=1, point_value=10)
            req2.endorsement = Endorsements(endorser=endorser,                   endorsee=endorsee_sus    ,              archive='cs', subject_class='CR',)

            req3 = EndorsementRequests(endorsee=endorsee,
                                    secret='end_sec_2',
                                    archive='cs', subject_class='CV',
                                    issued_when=datetime.now(),
                                    flag_valid=1, point_value=-10)
            req3.endorsement = Endorsements(endorser=endorser, endorsee=endorsee         ,                            archive='cs', subject_class='CV')

            req4 = EndorsementRequests(endorsee=endorsee,
                                    secret='end_sec_3',
                                    archive='cs', subject_class='DL',
                                    issued_when=datetime.now() - timedelta(days=4),
                                    flag_valid=1, point_value=10)
            req4.endorsement = Endorsements(endorser=endorser,                  endorsee=endorsee  ,                 archive='cs', subject_class='DL')

            session.commit()

    return app


def _settup_warnings(app):
    if not app.config['SQLALCHEMY_DATABASE_URI'] and not app.config['DEBUG']:
        logger.error("SQLALCHEMY_DATABASE_URI is not set!")

    if not app.config['WTF_CSRF_ENABLED'] and not(app.config['FLASK_DEBUG'] or app.config['DEBUG']):
        logger.warning("CSRF protection is DISABLED, Do not disable CSRF in production")
