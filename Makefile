.PHONY: all virtualenv install nopyc clean test test-smoke test-tavern test-tavern-smoke test-selenium test-selenium-smoke

PYTHON_BIN := python3
SHELL := /usr/bin/env bash
OS := $(shell uname)
CI_VENV ?= .venv
ENVIRONMENT ?= prod
AWS_REGION ?= us-east-1
PROJECT_APP_HOST ?= https://www.heliumedu.com
PROJECT_API_HOST ?= https://api.heliumedu.com

all: virtualenv install test

virtualenv:
	@if [ ! -d "$(CI_VENV)" ]; then \
		$(PYTHON_BIN) -m pip install virtualenv; \
        $(PYTHON_BIN) -m virtualenv $(CI_VENV); \
	fi

install: virtualenv
	@( \
		source $(CI_VENV)/bin/activate; \
		python -m pip install -r requirements.txt; \
	)

nopyc:
	find . -name '*.pyc' | xargs rm -f || true
	find . -name __pycache__ | xargs rm -rf || true

clean: nopyc
	rm -rf $(CI_VENV)

test:
	@make test-tavern
	@make test-selenium

test-smoke:
	@make test-tavern-smoke
	@make test-selenium-smoke

test-tavern:
	@( \
		source $(CI_VENV)/bin/activate; \
		ENVIRONMENT=$(ENVIRONMENT) \
		AWS_REGION=$(AWS_REGION) \
		PROJECT_APP_HOST=$(PROJECT_APP_HOST) \
		PROJECT_API_HOST=$(PROJECT_API_HOST) \
		PYTHONPATH=src/tavern:$$PYTHONPATH pytest -v src/tavern/init/test_setup.tavern.yaml src/tavern/tests/ src/tavern/init/test_teardown.tavern.yaml -s --log-cli-level info; \
	)

test-tavern-smoke:
	@( \
		source $(CI_VENV)/bin/activate; \
		ENVIRONMENT=$(ENVIRONMENT) \
		AWS_REGION=$(AWS_REGION) \
		PROJECT_APP_HOST=$(PROJECT_APP_HOST) \
		PROJECT_API_HOST=$(PROJECT_API_HOST) \
		PYTHONPATH=src/tavern:$$PYTHONPATH pytest -v src/tavern/tests/test_api_info.tavern.yaml src/tavern/tests/test_api_status.tavern.yaml -s --log-cli-level info; \
	)

test-selenium:
	@( \
		source $(CI_VENV)/bin/activate; \
		ENVIRONMENT=$(ENVIRONMENT) \
		AWS_REGION=$(AWS_REGION) \
		PROJECT_APP_HOST=$(PROJECT_APP_HOST) \
		PROJECT_API_HOST=$(PROJECT_API_HOST) \
		PYTHONPATH=src/selenium:src/tavern/utils:$$PYTHONPATH pytest -v src/selenium/init/test_setup.py src/selenium/tests/ src/selenium/init/test_teardown.py -s; \
	)

test-selenium-smoke:
	@( \
		source $(CI_VENV)/bin/activate; \
		ENVIRONMENT=$(ENVIRONMENT) \
		AWS_REGION=$(AWS_REGION) \
		PROJECT_APP_HOST=$(PROJECT_APP_HOST) \
		PROJECT_API_HOST=$(PROJECT_API_HOST) \
		PYTHONPATH=src/selenium:src/tavern/utils:$$PYTHONPATH pytest -v src/selenium/tests/test_pages.py src/selenium/tests/test_redirects.py -s; \
	)
