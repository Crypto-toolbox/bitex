.PHONY: install install-dev install-ci install-test tests lint style black black-check isort isort-check flake8 tag publish
SHELL := /bin/bash

install:
	pip install .

install-dev:
	pip install ".[dev]"

install-test:
	pip install ".[test]"

install-ci: install-dev install-test
	pip install flit twine

tests:
	cd tests/ && pytest --cov=bitex --disable-warnings -vvv

black:
	black bitex

isort:
	isort --recursive bitex

isort-check:
	isort --recursive --diff --check-only bitex

black-check:
	black --check --diff bitex

flake8:
	flake8 bitex

style: isort black

lint: flake8 black-check isort-check

checks: lint tests

tag-type:
	@bash .circleci/tag_type.sh

tag-feature:
	@echo Tagging new Feature
	bumpversion minor --verbose
	@echo tag commit

tag-patch:
	@echo Tagging new Patch
	bumpversion patch --verbose
	@echo tag commit

publish: lint tests
	@echo Publish to pypi