# admin-webapp

This repo provides a web app for for admin tools, forms, reports and APIs.

# How to get started
```bash
cd $HOME/arxiv # Or, your desired location
git clone git@github.com:arXiv/admin-webapp.git
cd admin-webapp
# git switch tapir-dev
make run
```

Makefile sets up the "venv" and runs script/run_local.sh after bootstrapping the environment.

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

While developing, it's best to open up dev.arxiv.org/admin for legacy Tapir so you can make changes freely. In some cases it can be helpful to open up production Tapir at arxiv.org/admin, but tread carefully so you don't unintentionally modify a user profile. In most cases, however, there isn't too much to worry about.

# Database Schema

Since there are several db schemata running around, this application makes some assumptions. They are a) a Moderators table in associative_tables.py in `arxiv-db` cannot exist and b) in the tapir_users.py file in `arxiv-db` the tapir_nickanames field needs to be one to one which means `useList` needs to be set to `false`.

# Running the tests

After setting up you should be able to run the tests with
`pytest`. This will create a sqlite db in a file and use that during
testing.

# Contributing
See [CONTRIBUTING](./CONTRIBUTING.md)
