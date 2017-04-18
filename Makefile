.DEFAULT: test
test:
	flake8 --append-config=flake8-required.cfg
	mypy .
	pytest tests

setup:
	virtualenv -p python3 venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -I -r requirements.txt
