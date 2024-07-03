# RUN FROM ROOT DIR OF REPO (Wherever Dockerfile lives)

docker build . -t admin-webapp
docker run \
    -e CLASSIC_DB_URI=sqlite:///:memory: \
    -e DEFAULT_LOGIN_REDIRECT_URL='/protected' \
    -e AUTH_SESSION_COOKIE_DOMAIN='localhost.arxiv.org' \
    -e CLASSIC_COOKIE_NAME='LOCALHOST_DEV_admin_webapp_classic_cookie' \
    -e AUTH_SESSION_COOKIE_SECURE=0 \
    -e DEFAULT_LOGOUT_REDIRECT_URL='/login' \
    -e CREATE_DB=1 \
    -e REDIS_FAKE=1 \
    --publish 8080:8080 \
    admin-webapp