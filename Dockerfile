FROM python:3.11.8-bookworm
RUN apt-get update && apt-get -y upgrade

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.3.2 \
    TRACE=1 \
    LC_ALL=en_US.utf8 \
    LANG=en_US.utf8 \
    APP_HOME=/app

WORKDIR /app

RUN apt-get -y install default-libmysqlclient-dev

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install -U pip "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

RUN pip install "gunicorn==20.1.0"

ADD admin_webapp /app/admin_webapp
ADD tests /app/tests

EXPOSE 8080

RUN useradd e-prints
RUN chown e-prints:e-prints /app/tests/data/
RUN chmod 775 /app/tests/data/
USER e-prints

ENV GUNICORN gunicorn --bind :8080 \
    --workers 4 --threads 8 --timeout 0 \
     "admin_webapp.factory:create_web_app()"

CMD exec $GUNICORN