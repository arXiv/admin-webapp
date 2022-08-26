# admin-webapp

This repo provides a web app for for admin tools, forms, reports and APIs.

# How to get started
```bash
cd admin-webapp
pip install poetry
poetry install  # installs to a venv
poetry shell    # activates the venv
pytest 
CLASSIC_DATABASE_URI=sqlite:///my.db FLASK_APP=accounts/app.py FLASK_DEBUG=1 flask run
```

To use MySQL/MariaDB:

```bash
poetry shell
CLASSIC_DATABASE_URI=mysql+mysqldb://[USERNAME]:[PASSWORD]@localhost:3306/[DATABASE] \
 FLASK_APP=app.py FLASK_DEBUG=1 flask run
```
Set the username, password, and database to whatever you're using. If
the DB structure does not already exist, you will need to be able to
create tables. Conventional read/write access should be sufficient.

You should be able to register a new user at
http://localhost:5000/register.


# Code style

All new code should adhere as closely as possible to
[PEP008](https://www.python.org/dev/peps/pep-0008/).

Use the [Numpy style](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt)
for docstrings.

## Linting

Use [Pylint](https://www.pylint.org/) to check your code prior to raising a
pull request. The parameters below will be used when checking code  cleanliness
on commits, PRs, and tags, with a target score of >= 9/10.

Here's how we use pylint in CI:

```bash
$ pipenv run pylint accounts/accounts users/arxiv/users
************* Module accounts.context
accounts/context.py:10: [W0212(protected-access), get_application_config] Access to a protected member _Environ of a client class
************* Module accounts.encode
accounts/encode.py:11: [E0202(method-hidden), ISO8601JSONEncoder.default] An attribute defined in json.encoder line 158 hides this method
************* Module accounts.controllers.baz
accounts/controllers/baz.py:1: [C0102(blacklisted-name), ] Black listed name "baz"
************* Module accounts.services.baz
accounts/services/baz.py:1: [C0102(blacklisted-name), ] Black listed name "baz"
************* Module accounts.services.things
accounts/services/things.py:11: [R0903(too-few-public-methods), Thing] Too few public methods (0/2)
accounts/services/things.py:49: [E1101(no-member), get_a_thing] Instance of 'scoped_session' has no 'query' member

------------------------------------------------------------------
Your code has been rated at 9.49/10 (previous run: 9.41/10, +0.07)
```

## Type hints and static checking
Use [type hint annotations](https://docs.python.org/3/library/typing.html)
wherever practicable. Use [mypy](http://mypy-lang.org/) to check your code.
If you run across typechecking errors in your code and you have a good reason
for `mypy` to ignore them, you should be able to add `# type: ignore`,
ideally along with an actual comment describing why the type checking should be
ignored on this line. In cases where it is hoped the types can be specified later,
just simplying adding the `# type: ignore` without further comment is fine.


Try running mypy with (from project root):

```bash
pipenv run mypy accounts users/arxiv | grep -v "test.*" | grep -v "defined here"
```

Mypy options are most easily specified by adding them to `mypy.ini` in the repo's
root directory.

mypy chokes on dynamic base classes and proxy objects (which you're likely
to encounter using Flask); it's perfectly fine to disable checking on those
offending lines using "``# type: ignore``". For example:

```python
>>> g.baz = get_session(app) # type: ignore
```
See [this issue](https://github.com/python/mypy/issues/500) for more
information.

