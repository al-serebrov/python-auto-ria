.DEFAULT: test
test:
	git diff | flake8 --diff
	pytest tests

setup:
	virtualenv -p python3 venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -I -r requirements.txt
