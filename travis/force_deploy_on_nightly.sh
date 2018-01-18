#!/bin/bash

if [[$TRAVIS_BRANCH == "nightly" ]]; then
    python generate_nightly_setup.py
    python setup.py sdist
    twine upload --username $PYPI_NAME --password $PYPI_PW dist/*
fi