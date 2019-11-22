.PHONY: install install-dev tests lint style black black-check isort isort-check flake8 tag publish
SHELL := /bin/bash
#COMMIT_SUBJECT=$(git log --format=oneline -n 1 HEAD --format=%s)
COMMIT_SUBJECT=FIXTURE

install:
	pip install .

install-dev:
	pip install ".[dev]"

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