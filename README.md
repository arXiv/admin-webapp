# admin-webapp

This repo provides a web app for for admin tools, forms, reports and APIs.

# How to get started
```bash
cd admin-webapp
pip install poetry
poetry install  # installs to a venv
poetry shell    # activates the venv
LOCALHOST_DEV=1 \
 python create_user.py  # fill out a test user
LOCALHOST_DEV=1 \
 FLASK_APP=admin_webapp/app.py \
 flask run
```
Then go to http://localhost.arxiv.org:5000/login and log in with the user and pw you just created.

To use with MySQL:

```bash
poetry shell
REDIS_FAKE=True FLASK_DEBUG=True FLASK_APP=admin_webapp/app.py \
 CLASSIC_DATABASE_URI=mysql+mysqldb://[USERNAME]:[PASSWORD]@localhost:3306/[DATABASE] \
 flask run
```
Set the username, password, and database to whatever you're using. If
the DB tables do not already exist, you will need to be able to
create tables. Conventional read/write access should be sufficient.

You should be able to go to a page like  http://localhost:5000/login  or  http://localhost:5000/register

# Build Notes
The `PyYAML` dependency may cause a build failure when using Python 3.10.x due to a breaking Cython change. For local development purposes, set `pyyaml = 5.3.x` in the `pyproject.toml` file then run `poetry install`.

# Running the tests

After setting up you should be able to run the tests with
`pytest`. This will create a sqlite db in a file and use that during
testing.

# Contributing
See [CONTRIBUTING](./CONTRIBUTING.md)
