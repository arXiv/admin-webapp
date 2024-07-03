export FLASK_APP=admin_webapp/app.py
export CLASSIC_DB_URI=sqlite:///test.db
export DEFAULT_LOGIN_REDIRECT_URL='/protected'
export AUTH_SESSION_COOKIE_DOMAIN='localhost.arxiv.org'
export CLASSIC_COOKIE_NAME='LOCALHOST_DEV_admin_webapp_classic_cookie'
export AUTH_SESSION_COOKIE_SECURE=0
export DEFAULT_LOGOUT_REDIRECT_URL='/login'
export REDIS_FAKE=1


# SET UP CONNECTION TO WRITABLE DB W/ DATA

poetry run python create_user.py
poetry run flask run