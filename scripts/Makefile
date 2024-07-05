HOST_PYTHON3=$(shell which python3)
VENV_BIN=venv/bin/
VENV_PYTHON3=${VENV_BIN}/python3

.PHONY: init mypy lint test checks

checks: init test mypy lint

init:
	${HOST_PYTHON3} -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

test:
	${VENV_BIN}/pytest .

mpypy:
	${VENV_BIN}/mypy .

lint:
	echo ${PYTHONPATH}
	PYTHONPATH=${PWD} ${VENV_BIN}/pylint .
