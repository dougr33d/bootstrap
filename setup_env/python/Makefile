PYTHON_VERSION=3.12.4
CWD=${PWD}

PY_BUILD_DIR=Python-${PYTHON_VERSION}
PY_TARBALL=Python-${PYTHON_VERSION}.tgz
PY_URL=https://www.python.org/ftp/python/${PYTHON_VERSION}/${PY_TARBALL}
PY_BIN=bin/python3

PY_INSTALL_PATH=${HOME}/tools/

.PHONY: init clean

init: ${PY_BIN}

clean: 
	rm -rf bin include lib share ${PY_BUILD_DIR}

${PY_BIN}: ${PY_BUILD_DIR}/configure
	#cd ${PY_BUILD_DIR} && ./configure --prefix=${PY_INSTALL_PATH}/ && make -j3 && make install
	@echo
	@echo
	@echo "Now, please add:"
	@echo
	@echo "  export PATH=$$PATH:${PY_BUILD_DIR}"
	@echo
	@echo "to ~/.bashrc"


${PY_BUILD_DIR}/configure: ${PY_TARBALL}
	tar xzf ${PY_TARBALL}


${PY_TARBALL}:
	curl ${PY_URL} -o ${PY_TARBALL}
