PYTHON := python3.11

default: .bootstrap

venv:
	${PYTHON} -m venv venv
	. venv/bin/activate && pip install --upgrade pip 
	. venv/bin/activate && pip install poetry
	. venv/bin/activate && poetry install

.bootstrap: venv
	touch .bootstrap

test.db: .bootstrap
	. venv/bin/activate && . ./.localenv && poetry run python create_user.py --password boguspassword --username bob --email bogus@example.com --first-name Bob --last-name Bogus --suffix-name '' --affiliation FSU --home-page https://asdf.com

run: test.db
	script/run_local.sh
