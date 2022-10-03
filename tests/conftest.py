"""Special pytest fixture configuration file.

This file automatically provides all fixtures defined in it to all
pytest tests in this directory and sub directories.

See https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files

pytest fixtures are used to initialize object for test functions. The
fixtures run for a function are based on the name of the argument to
the test function.

Scope = 'session' means that the fixture will be run onec and reused
for the whole test run session. The default scope is 'function' which
means that the fixture will be re-run for each test function.

"""
import pytest

from pathlib import Path
import hashlib
from base64 import b64encode

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from arxiv_db import test_load_db_file, models

from admin_webapp.factory import create_web_app

DB_FILE = "./pytest.db"

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE}"

CONNECT_ARGS = {"check_same_thread": False} if 'sqlite' in SQLALCHEMY_DATABASE_URL  \
    else {}

SQL_DATA_FILE = './tests/data/data.sql'

DELETE_DB_FILE_ON_EXIT = True



@pytest.fixture(scope='session')
def engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=CONNECT_ARGS)
    return engine


@pytest.fixture(scope='session')
def db(engine):
    """Create and load db tables."""
    print("Making tables...")
    try:
        from arxiv_db.tables import arxiv_tables
        arxiv_tables.metadata.create_all(bind=engine)
        print("Done making tables.")
        test_load_db_file(engine, SQL_DATA_FILE)
        yield engine
    finally: # cleanup
        if DELETE_DB_FILE_ON_EXIT:
            Path(DB_FILE).unlink(missing_ok=True)
            print(f"Deleted {DB_FILE}. Set DELETE_DB_FILE_ON_EXIT to control.")

@pytest.fixture(scope='session')
def admin_user(db):
    with Session(engine) as session:
        # We have a good old-fashioned user.
        db_user = models.TapirUsers(
            user_id=1,
            first_name='testadmin',
            last_name='admin',
            suffix_name='',
            email='testadmin@example.com',
            policy_class=2,
            flag_edit_users=1,
            flag_email_verified=1,
            flag_edit_system=0,
            flag_approved=1,
            flag_deleted=0,
            flag_banned=0,
                tracking_cookie='foocookie',
        )
        db_nick = models.TapirNicknames(
            nick_id=1,
            nickname='foouser',
            user_id=1,
            user_seq=1,
            flag_valid=1,
            role=0,
            policy=0,
            flag_primary=1
        )
        # db_demo = models.Demographics(
        #     user_id=1,
        #     country='US',
        #     affiliation='Cornell U.',
        #     url='http://example.com/bogus',
        #     rank=2,
        #     original_subject_classes='cs.OH',
        # )
        salt = b'fdoo'
        password = b'thepassword'
        hashed = hashlib.sha1(salt + b'-' + password).digest()
        encrypted = b64encode(salt + hashed)
        db_password = models.TapirUsersPassword(
            user_id=1,
            password_storage=2,
            password_enc=encrypted
        )
        session.add(db_user)
        session.add(db_password)
        session.add(db_nick)
        #session.add(db_demo)

        return db_user

@pytest.fixture(scope='session')
def secret():
    return f'bogus secret set in {__file__}'

@pytest.fixture(scope='session')
def app(db, secret, admin_user):
    """Flask client"""
    app = create_web_app()
    #app.config['CLASSIC_COOKIE_NAME'] = 'foo_tapir_session'
    #app.config['AUTH_SESSION_COOKIE_NAME'] = 'baz_session'
    app.config['AUTH_SESSION_COOKIE_SECURE'] = '0'
    app.config['JWT_SECRET'] = "jwt_" + secret
    app.config['CLASSIC_SESSION_HASH'] = "classic_hash_" +secret
    app.config['CLASSIC_DATABASE_URI'] = db.url
    app.config['SQLALCHEMY_DATABASE_URI'] = db.url
    app.config['REDIS_FAKE'] = True
    return app


@pytest.fixture
def user_ng_auth(userid):
    """Create a authenticated NG JWT."""
    return "TODO!"
