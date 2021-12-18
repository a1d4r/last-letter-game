#* Variables
SHELL := /usr/bin/env bash
PYTHON := python

#* Docker variables
IMAGE := game
VERSION := latest

#* Directories with source code
CODE = game tests
TESTS = tests

#* Poetry
.PHONY: poetry-download
poetry-download:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | $(PYTHON) -

.PHONY: poetry-remove
poetry-remove:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | $(PYTHON) - --uninstall

#* Installation
.PHONY: install
install:
	poetry install -n
	poetry run mypy --install-types --non-interactive $(CODE)

.PHONY: pre-commit-install
pre-commit-install:
	poetry run pre-commit install

#* Formatters
.PHONY: codestyle
codestyle:
	poetry run pyupgrade --exit-zero-even-if-changed --py39-plus **/*.py
	poetry run isort --settings-path pyproject.toml $(CODE)
	poetry run black --config pyproject.toml $(CODE)
	poetry run autoflake --recursive --in-place --remove-all-unused-imports --ignore-init-module-imports $(CODE)

.PHONY: format
format: codestyle

#* Test
.PHONY: test
test:
	poetry run pytest -c pyproject.toml

# Validate pyproject.toml
.PHONY: check-poetry
check-poetry:
	poetry check

#* Check code style
.PHONY: check-isort
check-isort:
	poetry run isort --diff --check-only --settings-path pyproject.toml $(CODE)

.PHONY: check-black
check-black:
	poetry run black --diff --check --config pyproject.toml $(CODE)

.PHONY: check-darglint
check-darglint:
	poetry run darglint --verbosity 2 $(CODE)

.PHONY: check-codestyle
check-codestyle: check-isort check-black check-darglint

#* Static linters

.PHONY: check-pylint
check-pylint:
	poetry run pylint --rcfile=pyproject.toml $(CODE)

.PHONY: check-mypy
check-mypy:
	poetry run mypy --config-file pyproject.toml $(CODE)

.PHONY: static-lint
static-lint: check-pylint check-mypy

#* Check security issues

.PHONY: check-bandit
check-bandit:
	poetry run bandit -ll -c pyproject.toml --recursive $(CODE)

.PHONY: check-safety
check-safety:
	poetry run safety check --full-report

.PHONY: check-security
check-security:
	poetry run safety check --full-report
	poetry run bandit -ll --recursive $(CODE)

.PHONY: lint
lint: check-poetry check-codestyle static-lint check-security

#* Docker
# Example: make docker VERSION=latest
# Example: make docker IMAGE=some_name VERSION=0.1.0
.PHONY: docker-build
docker-build:
	@echo Building docker $(IMAGE):$(VERSION) ...
	docker build \
		-t $(IMAGE):$(VERSION) . \
		-f ./docker/Dockerfile --no-cache

# Example: make clean_docker VERSION=latest
# Example: make clean_docker IMAGE=some_name VERSION=0.1.0
.PHONY: docker-remove
docker-remove:
	@echo Removing docker $(IMAGE):$(VERSION) ...
	docker rmi -f $(IMAGE):$(VERSION)

#* Cleaning
.PHONY: pycache-remove
pycache-remove:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

	poetry install -n
.PHONY: build-remove
build-remove:
	rm -rf build/

.PHONY: clean-all
clean-all: pycache-remove build-remove docker-remove
