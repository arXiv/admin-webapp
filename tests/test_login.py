from flask import url_for


def test_can_get_login_form(client):
    resp = client.get(url_for('login'))
    assert resp.status_code == 200
