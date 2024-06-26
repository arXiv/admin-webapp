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
import os
import pytest

from pathlib import Path, PurePath
import hashlib
from base64 import b64encode
import pathlib

from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

from arxiv.db import models, transaction

from admin_webapp.factory import create_web_app

DB_FILE = "./pytest.db"


SQL_DATA_FILE = './tests/data/data.sql'

DELETE_DB_FILE_ON_EXIT = True

TEST_CONFIG = {
    'CLASSIC_COOKIE_NAME':'foo_tapir_session',
    'AUTH_SESSION_COOKIE_NAME':'baz_session',
    'AUTH_SESSION_COOKIE_SECURE':False,
    'SESSION_DURATION':500,
    'JWT_SECRET':'bazsecret',
    'CLASSIC_DB_URI':'sqlite:///db.sqlite',
    'CLASSIC_SESSION_HASH':'xyz1234',
    'REDIS_FAKE':True,
    'BASE_SERVER':'example.com',
    'CREATE_DB':True
}

def test_load_db_file(engine, test_data: str):
    """Loads the SQL from the `test_data` file into the `engine`"""

    def escape_bind(stmt):
        return stmt.replace(':0', '\\:0')

    with engine.connect() as db:
        cmd_count = 0
        badcmd = False
        print(f"Loading test data from file '{test_data}'...")
        with open(test_data) as sql:
            cmd = ""
            for ln, line in enumerate(map(escape_bind, sql)):
                try:
                    if line.startswith("--"):
                        continue
                    elif line and line.rstrip().endswith(";"):
                        cmd = cmd + line
                        if cmd:
                            #print(f"About to run '{cmd}'")
                            db.execute(text(cmd))
                            cmd_count = cmd_count + 1
                            cmd = ""
                        else:
                            #print("empty command")
                            cmd = ""
                    elif not line and cmd:
                        #print(f"About to run '{cmd}'")
                        db.execute(text(cmd))
                        cmd_count = cmd_count + 1
                        cmd = ""
                    elif not line:
                        continue
                    else:
                        cmd = cmd + line
                except Exception as err:
                    badcmd = f"At line {ln} Running command #{cmd_count}. {err}"
                    break

        if badcmd:
            # moved this out of the except to avoid pytest printing huge stack traces
            raise Exception(badcmd)
        else:
            print(f"Done loading test data. Ran {cmd_count} commands.")

def parse_cookies(cookie_data):
    """This should be moved to a library function in arxiv-auth for reuse in tests."""
    cookies = {}
    for cdata in cookie_data:
        parts = cdata.split('; ')
        data = parts[0]
        key, value = data[:data.index('=')], data[data.index('=') + 1:]
        extra = {
            part[:part.index('=')]: part[part.index('=') + 1:]
            for part in parts[1:] if '=' in part
        }
        cookies[key] = dict(value=value, **extra)
    return cookies

@pytest.fixture(scope='session')
def app_with_db():
    app = create_web_app(**TEST_CONFIG)
    app.config['SERVER_NAME'] = 'example.com'
    try:
        yield app
    finally:
        try:
            os.remove(TEST_CONFIG['CLASSIC_DB_URI'])
        except:
            pass

@pytest.fixture(scope='session')
def app_with_populated_db():
    app = create_web_app(**TEST_CONFIG)
    app.config['SERVER_NAME'] = 'example.com'
    test_load_db_file(app.engine, SQL_DATA_FILE)
    try:
        yield app
    finally:
        try:
            os.remove(TEST_CONFIG['CLASSIC_DB_URI'])
        except:
            pass

@pytest.fixture(scope='session')
def engine():
    db_file = pathlib.Path(DB_FILE).resolve()
    try:
        print(f"Created db at {db_file}")
        connect_args = {"check_same_thread": False}
        engine = create_engine(f"sqlite:///{db_file}",
                               connect_args=connect_args)
        yield engine
    finally: # cleanup
        if DELETE_DB_FILE_ON_EXIT:
            db_file.unlink(missing_ok=True)
            print(f"Deleted {db_file} at end of test. "
                  "Set DELETE_DB_FILE_ON_EXIT to control.")

@pytest.fixture(scope='session')
def db(engine):
    """Create and load db tables."""
    print("Making tables...")
    from arxiv.db import Base
    Base.metadata.create_all(bind=engine)
    print("Done making tables.")
    test_load_db_file(engine, SQL_DATA_FILE)
    yield engine

@pytest.fixture(scope='session')
def admin_user(app_with_db):
    with app_with_db.app_context():
        with transaction() as session:
            admin_exists = select(models.TapirUser).where(models.TapirUser.email == 'testadmin@example.com')
            admin = session.scalar(admin_exists)
            if admin:
                return {
                    'email':'testadmin@example.com',
                    'password_cleartext':b'thepassword'
                }

            salt = b'fdoo'
            password = b'thepassword'
            hashed = hashlib.sha1(salt + b'-' + password).digest()
            encrypted = b64encode(salt + hashed)

            # We have a good old-fashioned user.
            db_user = models.TapirUser (
                user_id=59999,
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
            db_pw = models.TapirUsersPassword(
                user=db_user,
                password_storage=2,
                password_enc=encrypted
            )
            db_nick=models.TapirNickname(
                user_id = db_user.user_id,
                nickname='foouser',
                user_seq=1,
                flag_valid=1,
                role=0,
                policy=0,
                flag_primary=1
            )
            db_demo = models.Demographic(
                user_id=db_user.user_id,
                country='US',
                affiliation='Cornell U.',
                url='http://example.com/bogus',
                original_subject_classes='cs.OH',
                subject_class = 'OH',
                archive ='cs',
                type=5,
            )


            session.add(db_user)
            session.add(db_pw)
            session.add(db_nick)
            session.add(db_demo)

            session.commit()
            rd=dict(email=db_user.email, password_cleartext=password)
            return rd

@pytest.fixture(scope='session')
def secret():
    return f'bogus secret set in {__file__}'

@pytest.fixture(scope='session')
def app(db, secret, admin_user):
    """Flask client"""
    app = create_web_app()
    #app.config['CLASSIC_COOKIE_NAME'] = 'foo_tapir_session'
    #app.config['AUTH_SESSION_COOKIE_NAME'] = 'baz_session'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['AUTH_SESSION_COOKIE_SECURE'] = '0'
    app.config['JWT_SECRET'] = "jwt_" + secret
    app.config['CLASSIC_SESSION_HASH'] = "classic_hash_" +secret
    app.config['CLASSIC_DATABASE_URI'] = db.url
    app.config['SQLALCHEMY_DATABASE_URI'] = db.url
    app.config['REDIS_FAKE'] = True
    return app


@pytest.fixture(scope='session')
def admin_client(app_with_db, admin_user):
    """A flask app client pre configured to send admin cookies"""
    client = app_with_db.test_client()
    resp = client.post('/login', data=dict(username=admin_user['email'],
                                           password=admin_user['password_cleartext']))
    assert resp.status_code == 303
    cookies = parse_cookies(resp.headers.getlist('Set-Cookie'))
    ngcookie_name = app_with_db.config['AUTH_SESSION_COOKIE_NAME']
    assert ngcookie_name in cookies
    classic_cookie_name = app_with_db.config['CLASSIC_COOKIE_NAME']
    assert classic_cookie_name in cookies
    client.set_cookie(ngcookie_name, cookies[ngcookie_name]['value'])
    client.set_cookie(classic_cookie_name, cookies[classic_cookie_name]['value'])
    client.set_cookie(app_with_db.config['CLASSIC_TRACKING_COOKIE'], 'fake_browser_tracking_cookie_value')
    return client