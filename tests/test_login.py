from flask import url_for


def test_can_get_login_form(client):
    resp = client.get(url_for('login'))
    assert resp.status_code == 200

def test_can_login(client, admin_user, db):
    resp = client.post(url_for('login'),
                       data=dict(username=admin_user['email'],
                                 password=admin_user['password_cleartext']))
    assert resp.status_code == 303
