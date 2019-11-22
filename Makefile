.PHONY: install install-dev tests lint style black black-check isort isort-check flake8 tag publish

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

tag:
	@echo Detect part to bump
	@echo Bump detected part
	@echo tag commit

publish: lint tests
	@echo Publish to pypi