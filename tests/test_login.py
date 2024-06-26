from flask import url_for
from conftest import parse_cookies

def test_can_get_login_form(client):
    resp = client.get(url_for('login'))
    assert resp.status_code == 200

def test_can_login(admin_user, app_with_db):
    with app_with_db.test_client() as client:
        resp = client.post(url_for('login'),
                        data=dict(username=admin_user['email'],
                                    password=admin_user['password_cleartext']))
    assert resp.status_code == 303

    cookies = parse_cookies(resp.headers.getlist('Set-Cookie'))
    ngcookie_name = app_with_db.config['AUTH_SESSION_COOKIE_NAME']
    assert ngcookie_name in cookies
    classic_cookie_name = app_with_db.config['CLASSIC_COOKIE_NAME']
    assert classic_cookie_name in cookies

def test_can_get_protected(admin_client):
    resp = admin_client.get('/protected')
    assert resp.status_code == 200
