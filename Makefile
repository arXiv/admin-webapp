PYTHON := python3.11

default: .bootstrap

venv:
	${PYTHON} -m venv venv
	. venv/bin/activate && pip install --upgrade pip 
	. venv/bin/activate && pip install poetry
	. venv/bin/activate && poetry install

.bootstrap: venv
	. venv/bin/activate && . .env && poetry run python create_user.py # SET UP CONNECTION TO WRITABLE DB W/ DATA
	touch .bootstrap

run: .bootstrap
	script/run_local.sh
