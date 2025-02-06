# admin-webapp

This repo provides a web app for for admin tools, forms, reports and APIs.

# How to get started
```bash
cd admin-webapp
pip install poetry
pip install "cython<3.0.0" && pip install --no-build-isolation pyyaml==6.0 # see below
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

# Running the tests

After setting up you should be able to run the tests with
`pytest`. This will create a sqlite db in a file and use that during
testing.

# what is the deal with the pyyaml install?
Pyyaml doesn't seem to build with cython. But some packages require a broken version.
We used a hack from see https://github.com/yaml/pyyaml/issues/724
This is only needed if the install of pyyaml gives an error about cython.

Once the packages are more modern this could be removed.


# Contributing
See [CONTRIBUTING](./CONTRIBUTING.md)
