.PHONY: tests

VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python

freeze:
	${PYTHON} -m pip freeze > requirements.txt

install:
	python3 -m pip install -U pip
	python3 -m venv $(VENV_NAME)
	${PYTHON} -m pip install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf htmlcov

fix:
	$(PYTHON) -m black ./src
	$(PYTHON) -m autopep8 --recursive --in-place --aggressive --aggressive ./src/*


analyse:
	$(PYTHON) -m flake8 ./src
	$(PYTHON) -m pylint ./src
	$(PYTHON) -m pycodestyle ./src

tests:
	$(PYTHON) -m pytest --cov=./src --cov-report=html
