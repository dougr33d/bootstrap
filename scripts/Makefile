HOST_PYTHON3=$(shell which python3.12)
VENV=venv
VENV_BIN=${VENV}/bin
VENV_PYTHON3=${VENV_BIN}/python3
PYTHON_SENTINEL=.python3.sentinel

.PHONY: init mypy lint test checks clean

checks: init test mypy lint

clean:
	rm -rf ${VENV} ${PYTHON_SENTINEL}

init: ${PYTHON_SENTINEL}

${PYTHON_SENTINEL}: requirements.txt
	${HOST_PYTHON3} -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt
	@touch ${PYTHON_SENTINEL}

test:
	PYTHONPATH=${PWD} ${VENV_BIN}/pytest .

mypy:
	PYTHONPATH=${PWD} ${VENV_BIN}/mypy . --explicit-package-bases

lint:
	PYTHONPATH=${PWD} ${VENV_BIN}/pylint .